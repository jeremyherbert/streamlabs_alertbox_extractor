import sys
import os
import json
import threading
import requests
import traceback

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from abc import ABC
import arrow

from simple_ui_list import Ui_MainWindow
import streamlabs


file_path = os.path.dirname(os.path.realpath(__file__))
ENCODING = 'utf-8'

def seconds_to_hms(seconds: int):
    tmp_seconds = seconds

    hours = int(tmp_seconds / 3600)
    tmp_seconds -= hours * 3600

    mins = int(tmp_seconds / 60)
    tmp_seconds -= mins * 60

    output_string = ""
    if hours:
        output_string += "%ih" % hours
    if mins:
        output_string += "%sm" % str(mins).zfill(2)

    output_string += "%ss" % str(int(tmp_seconds)).zfill(2)

    return output_string

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

    new_streamlabs_packet = pyqtSignal(list)
    blank_config = {
        "streamlabs_url": "",
        "twitch_client_id": "",
        "twitch_username": ""
    }

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._donations = []
        self._donation_timestamps = []
        self._list_items = []

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

        self.new_streamlabs_packet.connect(self._parse_streamlabs_blob)

        self._streamlabs_api = streamlabs.StreamlabsAPI()

        self._connection_status_thread = threading.Thread(target=self._update_connection_status, daemon=True)
        self._connection_status_thread.start()

        self._write_streamlabs_data_thread = threading.Thread(target=self._write_streamlabs_data_to_file, daemon=True)
        self._write_streamlabs_data_thread.start()

        # item = QtWidgets.QListWidgetItem()
        # self.listWidget.addItem(item)
        #
        # label = QtWidgets.QLabel()
        # label.setWordWrap(True)
        # label.setText("Started<br>hello<br><a href=\"https://google.com\">hi</a>")
        #
        # item.setSizeHint(label.sizeHint())
        # self.listWidget.setItemWidget(item, label)
        #
        # self.listWidget.removeItemWidget(item)

    def _write_streamlabs_data_to_file(self):
        for name in ["msglog.txt", "title.txt", "id.txt", "url.txt"]:
            with open(os.path.join(file_path, name), 'w', encoding=ENCODING) as f:
                f.write("")

        while 1:
            data = self._streamlabs_api.get_websocket_data_blocking()

            with open(os.path.join(file_path, "msglog.txt"), 'a', encoding=ENCODING) as f:
                f.write(json.dumps(data) + "\n\n")

            self.new_streamlabs_packet.emit(data)

            # testing only!
            # if len(data) >= 2 and type(data) is list and data[0] == "event":
            #     event_data = data[1]
            #     if event_data.get('type') == 'alertPlaying' and \
            #             event_data.get('message'):
            #         import time
            #         time.sleep(1)

    @pyqtSlot(list)
    def _parse_streamlabs_blob(self, blob):
        try:
            if len(blob) >= 2 and type(blob) is list and blob[0] == "event":
                event_data = blob[1]

                if event_data.get("type") == "donation" and type(event_data.get("message")) is list and \
                        event_data['message'][0].get("_id") and event_data['message'][0].get("media") and \
                        event_data['message'][0]['media'].get("duration"):

                    self._donations.append(event_data['message'][0])
                    self._donation_timestamps.append(arrow.now().timestamp)
                    self._recompute_queue_length()

                elif event_data.get('type') == 'alertPlaying' and \
                        event_data.get('message'):

                    label_text = ""
                    background_color = ""

                    if event_data['message'].get("type") == "donation":
                        donation_data = event_data['message']
                        background_color = "#aaffc3"

                        label_text += "Donation (amount: %s)<br>" % event_data['message'].get("amount")

                        if donation_data.get("message"):
                            msg = donation_data["message"]
                        else:
                            msg = "<i>(no message)</i>"
                        label_text += "From <b>%s</b>: %s<br><br>" % (donation_data.get("from"), msg)

                        if event_data.get('message').get('media'):
                            media_data = event_data['message']['media']

                            if media_data.get('type') == 'youtube' and \
                                    media_data.get('id') and \
                                    media_data.get('title') and \
                                    media_data.get('duration'):
                                duration = int(media_data['duration'] / 1000)
                                self._write_youtube_data(media_data['id'],
                                                         media_data['title'],
                                                         offset_sec=duration)

                                label_text += "Media (duration %s): <b>%s</b> - <a href=\"https://www.youtube.com/watch?v=%s\">%s</a>" % (seconds_to_hms(duration), media_data['title'], media_data['id'], media_data['id'])

                                # check if this donation was in the queue
                                found_index = -1
                                for i, donation in enumerate(self._donations):
                                    if donation['_id'] == donation_data['_id']:
                                        found_index = i
                                        break
                                else:
                                    pass

                                if found_index != -1:
                                    self.lblDonationDelay.setText("Donation to play delay: " + seconds_to_hms(arrow.now().timestamp - self._donation_timestamps[found_index]))

                                    self._donations = self._donations[found_index+1:]
                                    self._donation_timestamps = self._donation_timestamps[found_index + 1:]
                                    self._recompute_queue_length()
                                else:
                                    print("missing from index")



                            else:
                                label_text += "Media: <i>(no media)</i>"
                        else:
                            label_text += "Media: <i>(no media)</i>"

                    elif event_data['message'].get("type") == "bits":
                        bits_data = event_data['message']
                        background_color = "#c3aaff"

                        label_text += "Cheer (amount: %s)<br>" % bits_data.get("amount")
                        if bits_data.get("message"):
                            msg = bits_data["message"]
                        else:
                            msg = "<i>(no message)</i>"
                        label_text += "From <b>%s</b>: %s" % (bits_data.get("from"), msg)

                    elif event_data['message'].get("type") == "subscription":
                        sub_data = event_data['message']
                        background_color = "#ffc3aa"

                        label_text += "Subscription (months: %s)<br>" % sub_data.get("months")
                        if sub_data.get("message"):
                            msg = sub_data["message"]
                        else:
                            msg = "<i>(no message)</i>"
                        label_text += "From <b>%s</b>: %s" % (sub_data.get("from"), msg)

                        print(len(sub_data.get("message")))

                    if label_text != "":
                        # add a blank item
                        self._list_items.append(QtWidgets.QListWidgetItem())
                        self.listWidget.addItem(self._list_items[-1])

                        # add the real item

                        new_label = QtWidgets.QLabel()
                        new_label.setText(label_text)
                        new_label.setWordWrap(True)
                        new_label.setStyleSheet("QLabel { background-color: %s; }" % background_color)

                        self._list_items.append(QtWidgets.QListWidgetItem())

                        self.listWidget.addItem(self._list_items[-1])
                        self.listWidget.setItemWidget(self._list_items[-1], new_label)

                        self._list_items[-1].setSizeHint(new_label.size())

                        self.listWidget.scrollToBottom()

        except Exception as e:
            traceback.print_exc()
            raise

    def _recompute_queue_length(self):
        time_ms = 0
        for donation in self._donations:
            if donation.get("media") and donation['media'].get("duration"):
                time_ms += int(donation['media']['duration'])

        self.lblTimeRemaining.setText("Time Remaining: %s" % seconds_to_hms(int(time_ms/1000)))

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
        # return None
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