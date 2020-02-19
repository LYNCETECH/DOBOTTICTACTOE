# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'level.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from boardGUI import Ui_board

class Ui_level(object):
    
    def __init__(self, window):
        self.main = window
        
    def setupUi(self, level):
        level.setObjectName("level")
        level.resize(1164, 773)
        self.keepingWindows=level
        level.setMaximumSize(QtCore.QSize(1164, 2581))
        level.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("71UU+enQH9L._AC_SY355_.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        level.setWindowIcon(icon)
        level.setLayoutDirection(QtCore.Qt.LeftToRight)
        level.setStyleSheet("background-color: rgb(0, 85, 127);")
        self.centralwidget = QtWidgets.QWidget(level)
        self.centralwidget.setObjectName("centralwidget")
        self.btnEasy = QtWidgets.QPushButton(self.centralwidget)
        self.btnEasy.setGeometry(QtCore.QRect(110, 460, 261, 111))
        font = QtGui.QFont()
        
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnEasy.setFont(font)
        self.btnEasy.setAutoFillBackground(False)
        self.btnEasy.setStyleSheet("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("unnamed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEasy.setIcon(icon1)
        self.btnEasy.setIconSize(QtCore.QSize(50, 50))
        self.btnEasy.setObjectName("btnEasy")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(470, 190, 221, 201))
        self.logo.setMaximumSize(QtCore.QSize(5000, 5000))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("71UU+enQH9L._AC_SY355_.jpg"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.lbhome = QtWidgets.QLabel(self.centralwidget)
        self.lbhome.setGeometry(QtCore.QRect(370, 50, 441, 111))
        font = QtGui.QFont()
        font.setFamily("PMingLiU-ExtB")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.lbhome.setFont(font)
        self.lbhome.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbhome.setObjectName("lbhome")
        self.btnDiff = QtWidgets.QPushButton(self.centralwidget)
        self.btnDiff.setGeometry(QtCore.QRect(440, 460, 291, 111))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnDiff.setFont(font)
        self.btnDiff.setAutoFillBackground(False)
        self.btnDiff.setStyleSheet("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;")
        self.btnDiff.setIcon(icon1)
        self.btnDiff.setIconSize(QtCore.QSize(50, 50))
        self.btnDiff.setObjectName("btnDiff")
        self.btnExpert = QtWidgets.QPushButton(self.centralwidget)
        self.btnExpert.setGeometry(QtCore.QRect(790, 460, 281, 111))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnExpert.setFont(font)
        self.btnExpert.setAutoFillBackground(False)
        
        self.btnExpert.setStyleSheet("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;")
        self.btnExpert.setIcon(icon1)
        self.btnExpert.setIconSize(QtCore.QSize(50, 50))
        self.btnExpert.setObjectName("btnExpert")
        self.btnExpert.clicked.connect(self.btnExpert_click)
        self.btnDiff.clicked.connect(self.btnDiff_click)
        self.btnEasy.clicked.connect(self.btnEasy_click)
        level.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(level)
        self.statusbar.setObjectName("statusbar")
        level.setStatusBar(self.statusbar)
        self.retranslateUi(level)
        QtCore.QMetaObject.connectSlotsByName(level)

    def retranslateUi(self, level):
        _translate = QtCore.QCoreApplication.translate
        level.setWindowTitle(_translate("level", "TIC TAC TOE"))
        self.btnEasy.setText(_translate("level", "FACILE"))
        self.lbhome.setText(_translate("level", "Choisissez votre niveau"))
        self.btnDiff.setText(_translate("level", "DIFFICILE"))
        self.btnExpert.setText(_translate("level", "EXPERT"))
        

        
    
    def start(self,leveln):
        self.keepingWindows.hide()
        self.MWindow = QtWidgets.QMainWindow()
        self.ui=Ui_board(False,leveln,self.keepingWindows)
        self.ui.setupUi(self.MWindow)
        self.MWindow.show()
        
    def quitApp(self):
        QtWidgets.QApplication.quit()
    
    def btnEasy_click(self):
        self._level=0
        self.start(self._level)
        
    def btnExpert_click(self):
        self._level=2
        self.start(self._level)
        
    def btnDiff_click(self):
        self._level=1
        self.start(self._level)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    level = QtWidgets.QMainWindow()
    ui = Ui_level()
    ui.setupUi(level)
    level.show()
    sys.exit(app.exec_())
