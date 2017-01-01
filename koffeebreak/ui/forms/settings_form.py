# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/forms/settings.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 272)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.workTimeSpinBox = QtWidgets.QSpinBox(Dialog)
        self.workTimeSpinBox.setFrame(True)
        self.workTimeSpinBox.setReadOnly(False)
        self.workTimeSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.workTimeSpinBox.setSpecialValueText("")
        self.workTimeSpinBox.setMinimum(1)
        self.workTimeSpinBox.setMaximum(90)
        self.workTimeSpinBox.setProperty("value", 25)
        self.workTimeSpinBox.setObjectName("workTimeSpinBox")
        self.horizontalLayout_4.addWidget(self.workTimeSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.timeOfShortBreakSpinBox = QtWidgets.QSpinBox(Dialog)
        self.timeOfShortBreakSpinBox.setPrefix("")
        self.timeOfShortBreakSpinBox.setMinimum(1)
        self.timeOfShortBreakSpinBox.setMaximum(30)
        self.timeOfShortBreakSpinBox.setProperty("value", 5)
        self.timeOfShortBreakSpinBox.setObjectName("timeOfShortBreakSpinBox")
        self.horizontalLayout_5.addWidget(self.timeOfShortBreakSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.timeOfLongBreakSpinBox = QtWidgets.QSpinBox(Dialog)
        self.timeOfLongBreakSpinBox.setMinimum(1)
        self.timeOfLongBreakSpinBox.setMaximum(60)
        self.timeOfLongBreakSpinBox.setProperty("value", 10)
        self.timeOfLongBreakSpinBox.setObjectName("timeOfLongBreakSpinBox")
        self.horizontalLayout_3.addWidget(self.timeOfLongBreakSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.workTimeWhenPostponeBreakSpinBox = QtWidgets.QSpinBox(Dialog)
        self.workTimeWhenPostponeBreakSpinBox.setMinimum(1)
        self.workTimeWhenPostponeBreakSpinBox.setMaximum(30)
        self.workTimeWhenPostponeBreakSpinBox.setProperty("value", 5)
        self.workTimeWhenPostponeBreakSpinBox.setObjectName("workTimeWhenPostponeBreakSpinBox")
        self.horizontalLayout_6.addWidget(self.workTimeWhenPostponeBreakSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.numberOfShortsBreaksSpinBox = QtWidgets.QSpinBox(Dialog)
        self.numberOfShortsBreaksSpinBox.setMaximum(10)
        self.numberOfShortsBreaksSpinBox.setProperty("value", 3)
        self.numberOfShortsBreaksSpinBox.setObjectName("numberOfShortsBreaksSpinBox")
        self.horizontalLayout_2.addWidget(self.numberOfShortsBreaksSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.statusLabel = QtWidgets.QLabel(Dialog)
        self.statusLabel.setStyleSheet("color: rgba(0,0,0,100);")
        self.statusLabel.setText("")
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel.setObjectName("statusLabel")
        self.verticalLayout.addWidget(self.statusLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.defaultPushButton = QtWidgets.QPushButton(Dialog)
        self.defaultPushButton.setObjectName("defaultPushButton")
        self.horizontalLayout.addWidget(self.defaultPushButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.closePushButton = QtWidgets.QPushButton(Dialog)
        self.closePushButton.setObjectName("closePushButton")
        self.horizontalLayout.addWidget(self.closePushButton)
        self.savePushButton = QtWidgets.QPushButton(Dialog)
        self.savePushButton.setObjectName("savePushButton")
        self.horizontalLayout.addWidget(self.savePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Work time"))
        self.workTimeSpinBox.setSuffix(_translate("Dialog", " min"))
        self.label.setText(_translate("Dialog", "Time of short break"))
        self.timeOfShortBreakSpinBox.setSuffix(_translate("Dialog", " min"))
        self.label_3.setText(_translate("Dialog", "Time of long break"))
        self.timeOfLongBreakSpinBox.setSuffix(_translate("Dialog", " min"))
        self.label_5.setText(_translate("Dialog", "Work time when postpone break"))
        self.workTimeWhenPostponeBreakSpinBox.setSuffix(_translate("Dialog", " min"))
        self.label_4.setText(_translate("Dialog", "Number of short breaks"))
        self.defaultPushButton.setText(_translate("Dialog", "Return to default"))
        self.closePushButton.setText(_translate("Dialog", "Close"))
        self.savePushButton.setText(_translate("Dialog", "Save"))

