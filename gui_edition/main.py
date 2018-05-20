import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtGui, QtWidgets, QtCore
from abc import ABC
from gui import Ui_StreamlabsExtractorWindow

from pendulum.datetime import DateTime
import pendulum


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


def create_read_only_item(item_data, colour=None):
    item = QtWidgets.QTableWidgetItem(item_data)
    item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
    if colour:
        item.setBackground(colour)
    return item


class StreamLabsEvent(ABC):
    def __init__(self, timestamp: DateTime, duration: int, username: str):
        self.timestamp = timestamp
        self.duration = duration
        self.username = username

    def get_details(self):
        raise NotImplementedError

    @property
    def event_type(self):
        raise NotImplementedError

    @property
    def pretty_timestamp(self):
        return self.timestamp.replace(microsecond=0).strftime("%H:%M:%S")

    @property
    def pretty_duration(self):
        return seconds_to_hms(self.duration)


class StreamLabsDonationEvent(StreamLabsEvent):
    def __init__(self, youtube_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.youtube_id = youtube_id

    @property
    def youtube_url(self):
        return "https://www.youtube.com/watch?v=" + self.youtube_id

    # @property
    # def clickable_youtube_url(self):
    #     return "<a href=\"%s\">%s</a>" % (self.youtube_url, self.youtube_url)

    def get_details(self):
        return self.youtube_url

    @property
    def event_type(self):
        return "Donation"


class SimpleQueue(object):
    def __init__(self):
        self._queue = []

    def push(self, key, obj):
        for i, data in enumerate(self._queue):
            current_key, current_obj = data

            if current_key > key:
                self._queue.insert(i, (key, obj))
                break
        else:
            self._queue.append((key, obj))

    def pop(self):
        return self._queue.pop(0)

    def __getitem__(self, item: int):
        return self._queue[item][1]

    def __contains__(self, obj):
        for data in self._queue:
            if data[1] == obj:
                return True
        else:
            return False

    def __len__(self):
        return len(self._queue)


class StreamlabsExtractor(QDialog, Ui_StreamlabsExtractorWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tblQueueData.horizontalHeader().setStretchLastSection(True)


        self._event_queue = SimpleQueue()
        self._event_queue.push(1, StreamLabsDonationEvent(
            youtube_id="-vLYmrhGncM",
            timestamp=pendulum.now(),
            username="jer_emy",
            duration=123
        ))
        self._event_queue.push(3, StreamLabsDonationEvent(
            youtube_id="-vLYmrhGncM",
            timestamp=pendulum.now(),
            username="jer_emy3",
            duration=123
        ))
        self._event_queue.push(2, StreamLabsDonationEvent(
            youtube_id="-vLYmrhGncM",
            timestamp=pendulum.now(),
            username="jer_emy2",
            duration=123
        ))

        self._sync_table(active_row=1)

        self.prgTimeRemaining.setFormat("3m remaining (finish time: 23:53)")

    def _sync_table(self, active_row=-1):
        self.tblQueueData.setRowCount(len(self._event_queue))

        cumulative_seconds = 0
        for i in range(len(self._event_queue)):
            event = self._event_queue[i]  # type: StreamLabsEvent

            if i == active_row:
                colour = QtGui.QColor(0x3a, 0xdd, 0x36)
            else:
                colour=None

            self.tblQueueData.setItem(i, 0, create_read_only_item(event.pretty_timestamp, colour=colour))
            self.tblQueueData.setItem(i, 1, create_read_only_item(event.event_type, colour=colour))
            self.tblQueueData.setItem(i, 2, create_read_only_item(event.pretty_duration, colour=colour))
            self.tblQueueData.setItem(i, 3, create_read_only_item(seconds_to_hms(cumulative_seconds), colour=colour))
            self.tblQueueData.setItem(i, 4, create_read_only_item(event.username, colour=colour))
            self.tblQueueData.setItem(i, 5, create_read_only_item(event.get_details(), colour=colour))

            cumulative_seconds += event.duration




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = StreamlabsExtractor()

    ui.show()
    sys.exit(app.exec_())


