import sys
import os
import json
import threading
import requests
import traceback

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5 import QtGui, QtWidgets, QtCore
from abc import ABC
import arrow

from simple_ui import Ui_MainWindow
import streamlabs


file_path = os.path.dirname(os.path.realpath(__file__))
ENCODING = 'utf-8'


def show_error(text):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText(text)
    msg.exec_()


def show_warn(text):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setWindowTitle("Warning")
    msg.setText(text)
    msg.exec_()


class StreamlabsExtractor(QMainWindow, Ui_MainWindow):

    blank_config = {
        "streamlabs_url": "",
        "twitch_client_id": "",
        "twitch_username": ""
    }

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._config_path = os.path.join(file_path, "streamlabs_extractor_config.json")

        try:
            with open(os.path.join(file_path, "log.txt"), 'a') as f:
                f.write("\n\nStarted at " + str(arrow.now().isoformat()) + "\n")
        except PermissionError:
            show_error("Could not write to files in the same folder as the executable. "
                       "You may need to run this program with administrator permissions.")

            sys.exit(1)

        self._load_config()
        self.btnConnect.clicked.connect(self._connect)

        self._streamlabs_api = streamlabs.StreamlabsAPI()

        self._connection_status_thread = threading.Thread(target=self._update_connection_status, daemon=True)
        self._connection_status_thread.start()

        self._write_streamlabs_data_thread = threading.Thread(target=self._write_streamlabs_data_to_file, daemon=True)
        self._write_streamlabs_data_thread.start()

    def _write_streamlabs_data_to_file(self):
        for name in ["msglog.txt", "title.txt", "id.txt", "url.txt"]:
            with open(os.path.join(file_path, name), 'w', encoding=ENCODING) as f:
                f.write("")

        while 1:
            data = self._streamlabs_api.get_websocket_data_blocking()

            with open(os.path.join(file_path, "msglog.txt"), 'a', encoding=ENCODING) as f:
                f.write(json.dumps(data) + "\n\n")

            try:
                if len(data) >= 2 and type(data) is list and data[0] == "event":
                    event_data = data[1]

                    if event_data.get('type') == 'alertPlaying' and \
                            event_data.get('message') and \
                            event_data.get('message').get('media'):

                        media_data = event_data['message']['media']

                        if media_data.get('type') == 'youtube' and \
                                media_data.get('id') and \
                                media_data.get('title') and \
                                media_data.get('duration'):
                            video_time_offset = int(event_data['message']['duration']/1000)
                            self._write_youtube_data(media_data['id'],
                                                     media_data['title'],
                                                     offset_sec=video_time_offset)
            except Exception as e:
                traceback.print_exc()

    def _check_twitch_client_id(self):
        url = "https://api.twitch.tv/helix/streams?user_login=" + self.txtUsername.text()

        try:
            req = requests.get(url, headers={"Client-ID": self.txtClientId.text()})
        except requests.exceptions.ConnectionError:
            return False

        if req.status_code != 200:
            return False

        return True

    def _get_twitch_data(self):
        url = "https://api.twitch.tv/helix/streams?user_login=" + self.txtUsername.text()

        try:
            req = requests.get(url, headers={"Client-ID": self.txtClientId.text()})
        except requests.exceptions.ConnectionError:
            print("Twitch connection error")
            return None

        if req.status_code != 200:
            print("Twitch response not 200")
            return None

        data = json.loads(req.text)
        data = data['data']

        if len(data) == 0:
            return None
        else:
            return data[0]

    def _write_youtube_data(self, video_id, title, offset_sec):
        twitch_data = self._get_twitch_data()

        youtube_url = "https://www.youtube.com/watch?v=" + video_id
        with open(os.path.join(file_path, "title.txt"), 'w', encoding=ENCODING) as f:
            f.write(title)
        with open(os.path.join(file_path, "id.txt"), 'w', encoding=ENCODING) as f:
            f.write(video_id)
        with open(os.path.join(file_path, "url.txt"), 'w', encoding=ENCODING) as f:
            f.write(youtube_url)
        with open(os.path.join(file_path, "log.txt"), 'a', encoding=ENCODING) as f:
            if twitch_data is not None:
                start_time = arrow.get(twitch_data['started_at'])
                now_time = arrow.utcnow()
                now_time.shift(seconds=offset_sec)
                timedelta = now_time - start_time

                hours = int(timedelta.seconds / 3600)
                mins = int((timedelta.seconds - hours * 3600) / 60)
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

            f.write(songdata)

            self.txtLastTimestamp.setText("%s:%s:%s" % (str(hours).zfill(2), str(mins).zfill(2), str(sec).zfill(2)))
            self.txtLastTitle.setText(title)
            self.txtLastUrl.setText(youtube_url)

    def _update_connection_status(self):
        while 1:
            self.lblStatus.setText("Disconnected")
            self.lblStatus.setStyleSheet("QLabel { color: red; }")
            self._streamlabs_api.connected_event.wait()
            self.lblStatus.setText("Connected to Streamlabs")
            self.lblStatus.setStyleSheet("QLabel { color: green; }")
            self._streamlabs_api.disconnected_event.wait()
            self.lblStatus.setText("Disconnected")
            self.lblStatus.setStyleSheet("QLabel { color: red; }")
            show_error("Streamlabs connection failed.")
            self._set_controls_disabled(False)

    def _write_default_config(self):
        with open(self._config_path, 'w', encoding=ENCODING) as f:
            f.write(json.dumps(StreamlabsExtractor.blank_config))

        return StreamlabsExtractor.blank_config

    def _load_config(self):
        if os.path.exists(self._config_path):
            with open(self._config_path, 'r', encoding=ENCODING) as f:
                data = f.read()

            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                show_error("Configuration was corrupted. You will need to reconfigure this program.")
                data = self._write_default_config()

            for key in StreamlabsExtractor.blank_config.keys():
                if key not in data:
                    show_error("Configuration was corrupted. You will need to reconfigure this program.")
                    data = self._write_default_config()
                    break

        else:
            data = self._write_default_config()

        self.txtStreamlabsUrl.setText(data['streamlabs_url'])
        self.txtClientId.setText(data['twitch_client_id'])
        self.txtUsername.setText(data['twitch_username'])

    def _save_config(self):
        with open(self._config_path, 'w', encoding=ENCODING) as f:
            f.write(json.dumps({
                "streamlabs_url": self.txtStreamlabsUrl.text(),
                "twitch_client_id": self.txtClientId.text(),
                "twitch_username": self.txtUsername.text(),
            }))

    def _validate(self):
        if not self.txtStreamlabsUrl.text().startswith("https://streamlabs.com/alert-box/v3/"):
            show_error("Streamlabs URL is invalid.")
            return False

        if self.txtClientId.text() == "":
            show_error("Twitch client ID is invalid.")
            return False

        if self.txtUsername.text() == "":
            show_error("Twitch username is invalid.")
            return False

        return True

    def _set_controls_disabled(self, state):
        self.btnConnect.setDisabled(state)
        self.txtStreamlabsUrl.setDisabled(state)
        self.txtUsername.setDisabled(state)
        self.txtClientId.setDisabled(state)

    def _connect(self):
        self._set_controls_disabled(True)
        self._save_config()
        if not self._validate():
            self._set_controls_disabled(False)
            return

        try:
            self._streamlabs_api.get_websocket_token(self.txtStreamlabsUrl.text())
        except streamlabs.NoWebsocketToken:
            show_error("Could not connect, no websocket token returned by streamlabs.")
            self._set_controls_disabled(False)
            return

        if not self._check_twitch_client_id():
            show_error("Twitch client ID was rejected by Twitch, or the connection to Twitch failed.")
            self._set_controls_disabled(False)
            return

        if self._get_twitch_data() is None:
            show_warn("The Twitch user '%s' is not yet streaming (double check the spelling!). Timestamps will not "
                      "work until the stream begins." % self.txtUsername.text())

        self._streamlabs_api.launch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = StreamlabsExtractor()

    ui.show()
    sys.exit(app.exec_())