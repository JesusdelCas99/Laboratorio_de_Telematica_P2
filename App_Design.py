# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:00:46 2020

@author: SoftLabs
"""
import torch
from PyQt5 import QtWidgets,uic

#Importamos modulos para computo cientifico
import numpy as np

#Importamos el modulo 'funciones.py' diseñadas
from Funciones import *

###########################################################################
################## PROGRAMACION BACK-END ##################################
###########################################################################

app=QtWidgets.QApplication([])

#Cargamos el archivo '.ui' diseñado mediante Qt Designer
dlg=uic.loadUi("VoIp_SoftLab.ui")

dlg.show()
app.exec()
