# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ArquitecturaDeRed.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1683, 948)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(880, 800, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(-20, -60, 1621, 951))
        self.label_2.setObjectName("label_2")
        self.NClientes = QtWidgets.QLabel(Dialog)
        self.NClientes.setGeometry(QtCore.QRect(10, 560, 55, 16))
        self.NClientes.setObjectName("NClientes")
        self.NLineas = QtWidgets.QLabel(Dialog)
        self.NLineas.setGeometry(QtCore.QRect(40, 390, 55, 16))
        self.NLineas.setObjectName("NLineas")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p><img src=\":/newPrefix/D:/Diseño de red(1)(1).png\"/></p></body></html>"))
        self.NClientes.setText(_translate("Dialog", "TextLabel"))
        self.NLineas.setText(_translate("Dialog", "TextLabel"))

import ArquitecturaDeRed_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

