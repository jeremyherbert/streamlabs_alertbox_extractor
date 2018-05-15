# -*- coding: utf-8 -*-
import asyncio
import websockets
import json
import requests
import argparse
import os
import arrow
import functools
import sys
import traceback

from colorama import init, Fore, Style
init()

ENCODING = 'utf-8'

def print_colour(colour, *args, **kwargs):
    print(colour, end='')
    print(*args, **kwargs)
    print(Style.RESET_ALL, end='')


printy = functools.partial(print_colour, Fore.YELLOW)
printg = functools.partial(print_colour, Fore.GREEN)
printr = functools.partial(print_colour, Fore.RED)
printdim = functools.partial(print_colour, Style.DIM)


def get_twitch_stream_data(username, client_id):
    url = "https://api.twitch.tv/helix/streams?user_login=" + username
    req = requests.get(url, headers={"Client-ID": client_id})

    if req.status_code != 200:
        raise RuntimeError("Twitch API responded with an error: " + req.text)

    data = json.loads(req.text)
    data = data['data']

    if len(data) == 0:
        printr("Twitch API reports that %s is not streaming. Timestamps will not work until they start." % username)
        return None
    elif len(data) == 1:
        return data[0]
    else:
        raise RuntimeError("Twitch reported multiple streams. This behaviour is not supported.")


def write_youtube_data(video_id, title, offset_sec=0):
    youtube_url = "https://www.youtube.com/watch?v=" + video_id
    twitch_data = get_twitch_stream_data(args['streamer'], args['clientid'])

    with open(os.path.join(args['output'], args['titlefile']), 'w', encoding=ENCODING) as f:
        f.write(title)
    with open(os.path.join(args['output'], args['idfile']), 'w', encoding=ENCODING) as f:
        f.write(video_id)
    with open(os.path.join(args['output'], args['urlfile']), 'w', encoding=ENCODING) as f:
        f.write(youtube_url)
    with open(os.path.join(args['output'], args['log']), 'a', encoding=ENCODING) as f:
        if twitch_data is not None:
            start_time = arrow.get(twitch_data['started_at'])
            now_time = arrow.utcnow()
            now_time.shift(seconds=offset_sec)
            timedelta = now_time - start_time

            hours = int(timedelta.seconds / 3600)
            mins = int((timedelta.seconds - hours*3600) / 60)
            sec = timedelta.seconds % 60
        else:
            hours = 0
            mins = 0
            sec = 0

        if hours:
            songdata = "%i:" % hours
        else:
            songdata = ""

        songdata += "%s:%s - %s - %s\n" % (
            str(mins).zfill(2),
            str(sec).zfill(2),
            youtube_url,
            title
        )

        printg("logging songdata:", songdata)
        f.write(songdata)


async def run(websocket_token):
    ws_url = "wss://aws-io.streamlabs.com:443/socket.io/?token=%s&EIO=3&transport=websocket" % websocket_token
    printy("streamlabs data URL is:", ws_url)
    async with websockets.connect(ws_url) as websocket:
        keepalive_task = asyncio.ensure_future(keepalive(websocket))
        read_data_task = asyncio.ensure_future(read_data(websocket))

        done, pending = await asyncio.wait(
            [keepalive_task, read_data_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()


ping_interval = 25


async def keepalive(socket):
    while 1:
        await asyncio.sleep(ping_interval)
        await socket.send("2")


async def read_data(socket):
    while 1:
        data = await socket.recv()

        data = data.strip()

        number = ""

        while data and data[0].isnumeric():
            number += data[0]
            data = data[1:]

        if data:
            parsed_data = json.loads(data)

            try:
                #printdim("%s:" % number, parsed_data)

                with open(os.path.join(args['output'], args['msglog']), 'a', encoding=ENCODING) as f:
                    f.write(json.dumps({"data": parsed_data, "now": str(arrow.utcnow())}) + "\n\n")

                if 'pingInterval' in parsed_data:
                    printy("Updating ping interval to", parsed_data['pingInterval'])
                    ping_interval = int(parsed_data['pingInterval']) / 1000

                # try:
                if len(parsed_data) and type(parsed_data) is list and parsed_data[0] == "event":
                    event_data = parsed_data[1]

                    if event_data['type'] == 'alertPlaying' and event_data['message'].get('media'):
                        media_data = event_data['message']['media']

                        if media_data['type'] == 'youtube':
                            video_time_offset = int(event_data['message']['duration']/1000)
                            write_youtube_data(media_data['id'],
                                               media_data['title'],
                                               offset_sec=video_time_offset)
                        else:
                            raise RuntimeError("Unknown media type")
            except Exception as e:
                traceback.print_exc(file=sys.stdout)

            else:
                printy("skipping unknown message")


        else:
            printdim("%s: <no data>" % number)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Takes youtube alert data from streamlabs and writes it to disk.")

    parser.add_argument('output',
                        help="The output directory for the text files")
    parser.add_argument('alerturl',
                        help="The streamlabs alertbox URL")
    parser.add_argument('clientid',
                        help="Twitch API client ID")
    parser.add_argument('streamer',
                        help="The name of the streamer to pull timestamps from")

    parser.add_argument('-t', '--titlefile', default="title.txt",
                        help="The title of the youtube video")
    parser.add_argument('-i', '--idfile', default="id.txt",
                        help="The youtube id of the video")
    parser.add_argument('-u', '--urlfile', default="url.txt",
                        help="The youtube url of the video")
    parser.add_argument('-l', '--log', default="log.txt",
                        help="A list of songs played and timestamps")
    parser.add_argument('-m', '--msglog', default="msglog.txt",
                        help="A list of all of the messages sent via streamlabs throughout the stream")

    args = vars(parser.parse_args())

    if get_twitch_stream_data(args['streamer'], args['clientid']) is None:
        pass

    printy("Clearing files...")
    for arg_file in ['titlefile', 'idfile', 'urlfile', 'msglog']:
        with open(os.path.join(args['output'], args[arg_file]), 'w', encoding=ENCODING) as f:
            f.write("")

    with open(os.path.join(args['output'], args['log']), 'a', encoding=ENCODING) as f:
        f.write("\n\n")
        f.write("Restarted at: " + arrow.now().isoformat() + "\n")

    token = args['alerturl'].split("/")[-1]
    token_url = "https://streamlabs.com/api/v5/io/info?token=" + token
    valid_headers = {
        "Host": "streamlabs.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0",
        "Referer": args['alerturl'],
    }
    req = requests.get(token_url, headers=valid_headers)

    if req.status_code != 200:
        raise RuntimeError("Streamlabs server raised error: " + str(req.status_code))

    req_parsed = json.loads(req.text)
    websocket_token = req_parsed['path'].split("=")[-1]
    printg("got streamlabs websocket token!")

    asyncio.get_event_loop().run_until_complete(run(websocket_token))
