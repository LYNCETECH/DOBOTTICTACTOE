# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:58:28 2020

@author: CLARVIE
"""
import sys 
from PyQt5 import QtWidgets
from mainGUI import Ui_MainWindow


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())