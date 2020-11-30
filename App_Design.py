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
    dlg4.show()    
    
    dlg4.lineEdit_2.setText(dlg.lineEdit_9.text()) 
    dlg4.lineEdit_2.setReadOnly(True)
    
    Nc=float(dlg.lineEdit.text())
    NI=float(dlg.lineEdit_2.text())
    Tpll=float(dlg.lineEdit_4.text())
    Pll=float(dlg.lineEdit_5.text())
    
    BHT=(Nc*NI*Tpll*Pll)/60
    dlg4.TraficoBHT.setText(str(BHT) + " Erlangs")
    dlg4.TraficoBHT.setReadOnly(True)
    
    dlg4.lineEdit_3.setText(str(Erlang_B2(BHT,float(dlg.lineEdit_9.text()))))
    dlg4.lineEdit_3.setReadOnly(True)
########################################################################### 
    
def Paso2():  
    dlg2.show() 
    
    MOS=float(dlg.lineEdit_8.text())
    
    dlg2.lineEdit.setText(dlg.lineEdit_8.text())
    dlg2.lineEdit.setReadOnly(True)
    

###########################################################################
################## PROGRAMACION BACK-END ##################################
###########################################################################

app=QtWidgets.QApplication([])

#Cargamos el archivo '.ui' diseñado mediante Qt Designer
dlg=uic.loadUi("VoIp_SoftLab.ui")
dlg2=uic.loadUi("Paso2.ui")
dlg4=uic.loadUi("Paso4.ui")


#Placeholders, ¿usar en otros campos?
dlg.lineEdit_5.setPlaceholderText("Probabilidad entre 0-1")
dlg.lineEdit_9.setPlaceholderText("0-1")




dlg.pushButton.clicked.connect(Paso2) # Pops new window when pushed
dlg2.pushButton.clicked.connect(Paso4)

dlg.show()
app.exec()
