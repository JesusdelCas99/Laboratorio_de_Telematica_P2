# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:00:46 2020

@author: SoftLabs
"""

from PyQt5 import QtWidgets,uic

#Importamos modulos para computo cientifico
import numpy as np

#Importamos el modulo 'funciones.py' diseñadas
from Funciones import *

# Calculo de GoS número de líneas en una ventana adicional #################

def Paso4():
    dlg2.show()    
    
    dlg2.lineEdit_2.setText(dlg.lineEdit_9.text()) 
    dlg2.lineEdit_2.setReadOnly(True)
    
    Nc=float(dlg.lineEdit.text())
    NI=float(dlg.lineEdit_2.text())
    Tpll=float(dlg.lineEdit_4.text())
    Pll=float(dlg.lineEdit_5.text())
    
    BHT=(Nc*NI*Tpll*Pll)/60
    dlg2.TraficoBHT.setText(str(BHT) + " Erlangs")
    dlg2.TraficoBHT.setReadOnly(True)
    
    dlg2.lineEdit_3.setText(str(Erlang_B2(BHT,float(dlg.lineEdit_9.text()))))
    dlg2.lineEdit_3.setReadOnly(True)
###########################################################################   

###########################################################################
################## PROGRAMACION BACK-END ##################################
###########################################################################

app=QtWidgets.QApplication([])

#Cargamos el archivo '.ui' diseñado mediante Qt Designer
dlg=uic.loadUi("VoIp_SoftLab.ui")
dlg2=uic.loadUi("PruebaPaso4.ui")


#Placeholders, ¿usar en otros campos?
dlg.lineEdit_5.setPlaceholderText("Probabilidad entre 0-1")
dlg.lineEdit_9.setPlaceholderText("0-1")

dlg.pushButton.clicked.connect(Paso4) # Pops new window when pushed

dlg.show()
app.exec()
