# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_ui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(530, 303)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txtStreamlabsUrl = QtWidgets.QLineEdit(self.groupBox)
        self.txtStreamlabsUrl.setObjectName("txtStreamlabsUrl")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtStreamlabsUrl)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txtClientId = QtWidgets.QLineEdit(self.groupBox)
        self.txtClientId.setObjectName("txtClientId")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtClientId)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txtUsername = QtWidgets.QLineEdit(self.groupBox)
        self.txtUsername.setObjectName("txtUsername")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txtUsername)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblStatus = QtWidgets.QLabel(self.groupBox)
        self.lblStatus.setObjectName("lblStatus")
        self.horizontalLayout.addWidget(self.lblStatus)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnConnect = QtWidgets.QPushButton(self.groupBox)
        self.btnConnect.setObjectName("btnConnect")
        self.horizontalLayout.addWidget(self.btnConnect)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.line.raise_()
        self.verticalLayout.addWidget(self.groupBox)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.txtLastTitle = QtWidgets.QLineEdit(self.centralwidget)
        self.txtLastTitle.setReadOnly(True)
        self.txtLastTitle.setObjectName("txtLastTitle")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtLastTitle)
        self.txtLastUrl = QtWidgets.QLineEdit(self.centralwidget)
        self.txtLastUrl.setReadOnly(True)
        self.txtLastUrl.setObjectName("txtLastUrl")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtLastUrl)
        self.txtLastTimestamp = QtWidgets.QLineEdit(self.centralwidget)
        self.txtLastTimestamp.setReadOnly(True)
        self.txtLastTimestamp.setObjectName("txtLastTimestamp")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txtLastTimestamp)
        self.verticalLayout.addLayout(self.formLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Streamlabs Extractor"))
        self.groupBox.setTitle(_translate("MainWindow", "Configuration"))
        self.label.setText(_translate("MainWindow", "Streamlabs Alertbox URL:"))
        self.label_2.setText(_translate("MainWindow", "Twitch Client ID:"))
        self.label_3.setText(_translate("MainWindow", "Twitch Username:"))
        self.lblStatus.setText(_translate("MainWindow", "Disconnected"))
        self.btnConnect.setText(_translate("MainWindow", "Connect"))
        self.label_4.setText(_translate("MainWindow", "Last video title:"))
        self.label_5.setText(_translate("MainWindow", "Last video URL:"))
        self.label_6.setText(_translate("MainWindow", "Last stream timestamp: "))
