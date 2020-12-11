# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 21:17:14 2020

@author: Jesus
"""

from PyQt5 import QtWidgets,uic




app=QtWidgets.QApplication([])

dlg_aviso=uic.loadUi("Aviso.ui")
dlg_aviso.show()


app.exec()