import json
import requests
import websockets
import asyncio
import threading
import queue
import arrow
import traceback

class NoWebsocketToken(Exception):
    pass


class StreamlabsAPI(object):
    def __init__(self):
        self._alertbox_url = None
        self._websocket_token = None

        self._websocket_data = queue.Queue()
        self._ping_interval = 25
        self._last_ping_response = None

        self._thread = None  # type: threading.Thread

        self._disconnected_event = threading.Event()
        self._disconnected_event.set()
        self._connected_event = threading.Event()
        self._connected_event.clear()

    @property
    def connected_event(self):
        return self._connected_event

    @property
    def disconnected_event(self):
        return self._disconnected_event

    def get_websocket_token(self, alertbox_url):
        self._alertbox_url = alertbox_url
        self._websocket_token = self._get_websocket_token()

        if not self._websocket_token:
            raise NoWebsocketToken()

    def launch(self):
        if self._thread is None or not self._thread.is_alive():
            self._launch_background_thread()

    def get_websocket_data_blocking(self, timeout=None):
        return self._websocket_data.get(timeout=timeout)

    def _get_websocket_token(self):
        try:
            token = self._alertbox_url.split("/")[-1]
            token_url = "https://streamlabs.com/api/v5/io/info?token=" + token
            valid_headers = {
                "Host": "streamlabs.com",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0",
                "Referer": self._alertbox_url,
            }
            try:
                req = requests.get(token_url, headers=valid_headers)
            except requests.exceptions.ConnectionError:
                return None

            if req.status_code != 200:
                return None

            try:
                req_parsed = json.loads(req.text)
            except json.JSONDecodeError:
                return None
            websocket_token = req_parsed['path'].split("=")[-1]
        except Exception as e:
            traceback.print_exc()
            return None

        return websocket_token

    def _launch_background_thread(self):
        def loop_in_thread(asyncio_loop):
            asyncio.set_event_loop(asyncio_loop)
            asyncio_loop.run_until_complete(self._run())

        loop = asyncio.get_event_loop()
        self._thread = threading.Thread(target=loop_in_thread, args=(loop,), daemon=True)
        self._thread.start()

    async def _run(self):
        ws_url = "wss://aws-io.streamlabs.com:443/socket.io/?token=%s&EIO=3&transport=websocket" % self._websocket_token
        async with websockets.connect(ws_url) as websocket:
            self._disconnected_event.clear()
            self._connected_event.set()

            self._last_ping_response = arrow.now()
            keepalive_task = asyncio.ensure_future(self._keepalive(websocket))
            read_data_task = asyncio.ensure_future(self._read_data(websocket))

            done, pending = await asyncio.wait(
                [keepalive_task, read_data_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            self._connected_event.clear()
            self._disconnected_event.set()

    async def _keepalive(self, socket):
        while 1:
            print("sending keepalive")
            await socket.send("2")
            await asyncio.sleep(3)

            diff = arrow.now() - self._last_ping_response
            if diff.total_seconds() > 5:
                raise RuntimeError("Ping failed")

            await asyncio.sleep(self._ping_interval-3)

    async def _read_data(self, socket):
        while 1:
            data = await socket.recv()
            data = data.strip()

            number = ""
            while data and data[0].isnumeric():
                number += data[0]
                data = data[1:]

            if number == "3":
                self._last_ping_response = arrow.now()

            if data:
                try:
                    parsed_data = json.loads(data)
                except json.JSONDecodeError:
                    print("unknown packet encountered")
                    continue

                print(parsed_data)

                if 'pingInterval' in parsed_data:
                    self._ping_interval = int(parsed_data['pingInterval']) / 1000
                else:
                    self._websocket_data.put(parsed_data)
