# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StreamlabsExtractorWindow(object):
    def setupUi(self, StreamlabsExtractorWindow):
        StreamlabsExtractorWindow.setObjectName("StreamlabsExtractorWindow")
        StreamlabsExtractorWindow.resize(1257, 571)
        self.verticalLayout = QtWidgets.QVBoxLayout(StreamlabsExtractorWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(StreamlabsExtractorWindow)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tblQueueData = QtWidgets.QTableWidget(self.tab)
        self.tblQueueData.setAlternatingRowColors(True)
        self.tblQueueData.setObjectName("tblQueueData")
        self.tblQueueData.setColumnCount(6)
        self.tblQueueData.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblQueueData.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblQueueData.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblQueueData.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblQueueData.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblQueueData.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblQueueData.setHorizontalHeaderItem(5, item)
        self.verticalLayout_3.addWidget(self.tblQueueData)
        self.prgTimeRemaining = QtWidgets.QProgressBar(self.tab)
        self.prgTimeRemaining.setStyleSheet(" QProgressBar::chunk {\n"
"     background-color: #3add36;\n"
"     width: 1px;\n"
" }\n"
"\n"
" QProgressBar {\n"
"     border: 2px solid grey;\n"
"     border-radius: 0px;\n"
"     text-align: center;\n"
" }")
        self.prgTimeRemaining.setProperty("value", 24)
        self.prgTimeRemaining.setObjectName("prgTimeRemaining")
        self.verticalLayout_3.addWidget(self.prgTimeRemaining)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txtStreamlabsUrl = QtWidgets.QLineEdit(self.tab_2)
        self.txtStreamlabsUrl.setObjectName("txtStreamlabsUrl")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtStreamlabsUrl)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txtTwitchClientId = QtWidgets.QLineEdit(self.tab_2)
        self.txtTwitchClientId.setObjectName("txtTwitchClientId")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtTwitchClientId)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txtTwitchUsername = QtWidgets.QLineEdit(self.tab_2)
        self.txtTwitchUsername.setObjectName("txtTwitchUsername")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txtTwitchUsername)
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtOutputFolder = QtWidgets.QLineEdit(self.tab_2)
        self.txtOutputFolder.setReadOnly(True)
        self.txtOutputFolder.setObjectName("txtOutputFolder")
        self.horizontalLayout_2.addWidget(self.txtOutputFolder)
        self.btnBrowseForFolder = QtWidgets.QPushButton(self.tab_2)
        self.btnBrowseForFolder.setObjectName("btnBrowseForFolder")
        self.horizontalLayout_2.addWidget(self.btnBrowseForFolder)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.tab_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.line)
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.txtCfgYoutubeTitle = QtWidgets.QLineEdit(self.tab_2)
        self.txtCfgYoutubeTitle.setObjectName("txtCfgYoutubeTitle")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.txtCfgYoutubeTitle)
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.txtCfgYoutubeUrl = QtWidgets.QLineEdit(self.tab_2)
        self.txtCfgYoutubeUrl.setReadOnly(False)
        self.txtCfgYoutubeUrl.setObjectName("txtCfgYoutubeUrl")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.txtCfgYoutubeUrl)
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.txtCfgYoutubeId = QtWidgets.QLineEdit(self.tab_2)
        self.txtCfgYoutubeId.setReadOnly(False)
        self.txtCfgYoutubeId.setObjectName("txtCfgYoutubeId")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.txtCfgYoutubeId)
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.txtCfgLog = QtWidgets.QLineEdit(self.tab_2)
        self.txtCfgLog.setReadOnly(False)
        self.txtCfgLog.setObjectName("txtCfgLog")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.txtCfgLog)
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.txtCfgBacklog = QtWidgets.QLineEdit(self.tab_2)
        self.txtCfgBacklog.setReadOnly(False)
        self.txtCfgBacklog.setObjectName("txtCfgBacklog")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.txtCfgBacklog)
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.txtCfgDebugLog = QtWidgets.QLineEdit(self.tab_2)
        self.txtCfgDebugLog.setReadOnly(False)
        self.txtCfgDebugLog.setObjectName("txtCfgDebugLog")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.txtCfgDebugLog)
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.line_2 = QtWidgets.QFrame(self.tab_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.line_2)
        self.cmbSaveDebugLog = QtWidgets.QComboBox(self.tab_2)
        self.cmbSaveDebugLog.setObjectName("cmbSaveDebugLog")
        self.cmbSaveDebugLog.addItem("")
        self.cmbSaveDebugLog.addItem("")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.cmbSaveDebugLog)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btnSaveConfig = QtWidgets.QPushButton(self.tab_2)
        self.btnSaveConfig.setObjectName("btnSaveConfig")
        self.horizontalLayout_3.addWidget(self.btnSaveConfig)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblStatus = QtWidgets.QLabel(StreamlabsExtractorWindow)
        self.lblStatus.setStyleSheet("QLabel {color: red}")
        self.lblStatus.setObjectName("lblStatus")
        self.horizontalLayout.addWidget(self.lblStatus)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btnConnect = QtWidgets.QPushButton(StreamlabsExtractorWindow)
        self.btnConnect.setObjectName("btnConnect")
        self.horizontalLayout.addWidget(self.btnConnect)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(StreamlabsExtractorWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StreamlabsExtractorWindow)

    def retranslateUi(self, StreamlabsExtractorWindow):
        _translate = QtCore.QCoreApplication.translate
        StreamlabsExtractorWindow.setWindowTitle(_translate("StreamlabsExtractorWindow", "Streamlabs Extractor"))
        item = self.tblQueueData.horizontalHeaderItem(0)
        item.setText(_translate("StreamlabsExtractorWindow", "Timestamp"))
        item = self.tblQueueData.horizontalHeaderItem(1)
        item.setText(_translate("StreamlabsExtractorWindow", "Event type"))
        item = self.tblQueueData.horizontalHeaderItem(2)
        item.setText(_translate("StreamlabsExtractorWindow", "Duration"))
        item = self.tblQueueData.horizontalHeaderItem(3)
        item.setText(_translate("StreamlabsExtractorWindow", "ETA"))
        item = self.tblQueueData.horizontalHeaderItem(4)
        item.setText(_translate("StreamlabsExtractorWindow", "Username"))
        item = self.tblQueueData.horizontalHeaderItem(5)
        item.setText(_translate("StreamlabsExtractorWindow", "Details"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("StreamlabsExtractorWindow", "Queue Data"))
        self.label.setText(_translate("StreamlabsExtractorWindow", "Streamlabs Alertbox URL:"))
        self.label_2.setText(_translate("StreamlabsExtractorWindow", "Twitch Developer Client ID:"))
        self.label_3.setText(_translate("StreamlabsExtractorWindow", "Twitch Username:"))
        self.label_4.setText(_translate("StreamlabsExtractorWindow", "Output folder:"))
        self.btnBrowseForFolder.setText(_translate("StreamlabsExtractorWindow", "Browse..."))
        self.label_11.setText(_translate("StreamlabsExtractorWindow", "Output filenames:"))
        self.label_7.setText(_translate("StreamlabsExtractorWindow", "YouTube title:"))
        self.txtCfgYoutubeTitle.setText(_translate("StreamlabsExtractorWindow", "title.txt"))
        self.label_6.setText(_translate("StreamlabsExtractorWindow", "YouTube URL:"))
        self.txtCfgYoutubeUrl.setText(_translate("StreamlabsExtractorWindow", "url.txt"))
        self.label_8.setText(_translate("StreamlabsExtractorWindow", "YouTube ID:"))
        self.txtCfgYoutubeId.setText(_translate("StreamlabsExtractorWindow", "id.txt"))
        self.label_9.setText(_translate("StreamlabsExtractorWindow", "Timestamped song log:"))
        self.txtCfgLog.setText(_translate("StreamlabsExtractorWindow", "log.txt"))
        self.label_12.setText(_translate("StreamlabsExtractorWindow", "Backlog time estimate:"))
        self.txtCfgBacklog.setText(_translate("StreamlabsExtractorWindow", "backlog_time.txt"))
        self.label_10.setText(_translate("StreamlabsExtractorWindow", "Debug log:"))
        self.txtCfgDebugLog.setText(_translate("StreamlabsExtractorWindow", "msglog.txt"))
        self.label_13.setText(_translate("StreamlabsExtractorWindow", "Save debug log?"))
        self.cmbSaveDebugLog.setItemText(0, _translate("StreamlabsExtractorWindow", "Yes"))
        self.cmbSaveDebugLog.setItemText(1, _translate("StreamlabsExtractorWindow", "No"))
        self.btnSaveConfig.setText(_translate("StreamlabsExtractorWindow", "Save Configuration"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("StreamlabsExtractorWindow", "Configuration"))
        self.label_5.setText(_translate("StreamlabsExtractorWindow", "<html><head/><body><p>Project homepage: <a href=\"https://github.com/jeremyherbert/streamlabs_alertbox_extractor\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/jeremyherbert/streamlabs_alertbox_extractor</span></a></p><p><br/></p><p>Shoutouts to simpleflips</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("StreamlabsExtractorWindow", "About"))
        self.lblStatus.setText(_translate("StreamlabsExtractorWindow", "Disconnected"))
        self.btnConnect.setText(_translate("StreamlabsExtractorWindow", "Connect"))
