# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from levelGUI import Ui_level

class Ui_Mode(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 767)
        self.keepingWindows=MainWindow
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("71UU+enQH9L._AC_SY355_.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(0, 85, 127);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.noCam = QtWidgets.QPushButton(self.centralwidget)
        self.cam = QtWidgets.QPushButton(self.centralwidget)
        self.noCam.setGeometry(QtCore.QRect(370, 490, 341, 131))
        self.cam.setGeometry(QtCore.QRect(370, 490, 341, 131))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.noCam.setFont(font)
        self.noCam.setAutoFillBackground(False)
        self.noCam.setStyleSheet("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;")
        self.cam.setFont(font)
        self.cam.setAutoFillBackground(False)
        self.cam.setStyleSheet("color: #333;\n"
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
        self.noCam.setIcon(icon1)
        self.noCam.setIconSize(QtCore.QSize(50, 50))
        self.noCam.setFlat(False)
        self.noCam.setObjectName("noCam")
        self.cam.setIcon(icon1)
        self.cam.setIconSize(QtCore.QSize(50, 50))
        self.cam.setFlat(False)
        self.cam.setObjectName("cam")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(370, 170, 321, 271))
        self.logo.setAutoFillBackground(False)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("RobotLAB Dobot Robotic Arm-1-2-3.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.lbhome = QtWidgets.QLabel(self.centralwidget)
        self.lbhome.setGeometry(QtCore.QRect(410, 30, 271, 111))
        font = QtGui.QFont()
        font.setFamily("PMingLiU-ExtB")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.lbhome.setFont(font)
        self.lbhome.setAutoFillBackground(False)
        self.lbhome.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbhome.setObjectName("lbhome")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.noCam.clicked.connect(self.noCam_click)
        self.cam.clicked.connect(self.cam_click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TIC TAC TOE"))
        self.noCam.setText(_translate("MainWindow", "NORMAL"))
        self.cam.setText(_translate("MainWindow", "CAMERA"))
        self.lbhome.setText(_translate("MainWindow", "TIC TAC TOE "))
    
    def noCam_click(self):
        self.keepingWindows.hide()
        self.MWindow = QtWidgets.QMainWindow()
        self.ui=Ui_level(self.keepingWindows,0)
        self.ui.setupUi(self.MWindow)
        self.MWindow.show()

    def cam_click(self):
        self.keepingWindows.hide()
        self.MWindow = QtWidgets.QMainWindow()
        self.ui=Ui_level(self.keepingWindows,1)
        self.ui.setupUi(self.MWindow)
        self.MWindow.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Mode()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
