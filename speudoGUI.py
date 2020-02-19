# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'speudo.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlgName(object):
    def setupUi(self, dlgName):
        dlgName.setObjectName("dlgName")
        dlgName.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("71UU+enQH9L._AC_SY355_.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgName.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgName)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(dlgName)
        self.lineEdit.setGeometry(QtCore.QRect(30, 90, 341, 51))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(dlgName)
        self.label.setGeometry(QtCore.QRect(30, 60, 101, 16))
        self.label.setObjectName("label")
        
        self.retranslateUi(dlgName)
        self.buttonBox.accepted.connect(dlgName.accept)
        self.buttonBox.rejected.connect(dlgName.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgName)

    def retranslateUi(self, dlgName):
        _translate = QtCore.QCoreApplication.translate
        dlgName.setWindowTitle(_translate("dlgName", "Speudo joueur humain"))
        self.label.setText(_translate("dlgName", "Speudo joueur"))
    
    


"""if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlgName = QtWidgets.QDialog()
    ui = Ui_dlgName()
    ui.setupUi(dlgName)
    dlgName.show()
    sys.exit(app.exec_())"""
