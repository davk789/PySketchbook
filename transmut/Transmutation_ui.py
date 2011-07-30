# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Transmutation.ui'
#
# Created: Fri Jul 29 21:55:54 2011
#      by: PyQt4 UI code generator 4.8.4
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
        Form.resize(1100, 1107)
        Form.setStyleSheet(_fromUtf8("QWidget {\n"
"    background-color:  black;\n"
"    color: yellow;\n"
"}"))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget_6 = QtGui.QWidget(Form)
        self.widget_6.setObjectName(_fromUtf8("widget_6"))
        self.gridLayout.addWidget(self.widget_6, 0, 0, 1, 1)
        self.widget_4 = QtGui.QWidget(Form)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.gridLayout.addWidget(self.widget_4, 0, 1, 1, 1)
        self.widget_7 = QtGui.QWidget(Form)
        self.widget_7.setObjectName(_fromUtf8("widget_7"))
        self.gridLayout.addWidget(self.widget_7, 0, 2, 1, 1)
        self.widget_5 = QtGui.QWidget(Form)
        self.widget_5.setObjectName(_fromUtf8("widget_5"))
        self.gridLayout.addWidget(self.widget_5, 1, 0, 1, 1)
        self.drawArea = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drawArea.sizePolicy().hasHeightForWidth())
        self.drawArea.setSizePolicy(sizePolicy)
        self.drawArea.setMinimumSize(QtCore.QSize(900, 900))
        self.drawArea.setObjectName(_fromUtf8("drawArea"))
        self.gridLayout.addWidget(self.drawArea, 1, 1, 1, 1)
        self.widget_3 = QtGui.QWidget(Form)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.gridLayout.addWidget(self.widget_3, 1, 2, 1, 1)
        self.widget_9 = QtGui.QWidget(Form)
        self.widget_9.setObjectName(_fromUtf8("widget_9"))
        self.gridLayout.addWidget(self.widget_9, 2, 0, 1, 1)
        self.widget_2 = QtGui.QWidget(Form)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout.addWidget(self.widget_2, 2, 1, 1, 1)
        self.widget_8 = QtGui.QWidget(Form)
        self.widget_8.setObjectName(_fromUtf8("widget_8"))
        self.gridLayout.addWidget(self.widget_8, 2, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Transmutation Study", None, QtGui.QApplication.UnicodeUTF8))

