# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/SigilWindow.ui'
#
# Created: Wed Jun 29 23:33:26 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(752, 565)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.controlBox = QtGui.QVBoxLayout()
        self.controlBox.setObjectName(_fromUtf8("controlBox"))
        self.refreshButton = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy)
        self.refreshButton.setObjectName(_fromUtf8("refreshButton"))
        self.controlBox.addWidget(self.refreshButton)
        self.saveButton = QtGui.QPushButton(Form)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.controlBox.addWidget(self.saveButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.controlBox.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.controlBox)
        self.drawArea = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drawArea.sizePolicy().hasHeightForWidth())
        self.drawArea.setSizePolicy(sizePolicy)
        self.drawArea.setObjectName(_fromUtf8("drawArea"))
        self.horizontalLayout.addWidget(self.drawArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshButton.setText(QtGui.QApplication.translate("Form", "refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("Form", "save", None, QtGui.QApplication.UnicodeUTF8))

