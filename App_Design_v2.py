# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:00:46 2020

@author: SoftLabs
"""

from PyQt5 import QtWidgets,uic

#Importamos modulos para computo cientifico
import numpy as np

#Importamos las liberías pertinentes para el trabajo con la base de datos
import sqlite3 as sql
import pandas as pd

#Importamos el modulo 'funciones.py' diseñadas
from Funciones import *

#Importamos librerias para el cálculo de MOS
import math


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
    # print("El MOS de entrada es:",MOS)
    
    conn = sql.connect('PruebaDB.db')
    cursor = conn.cursor()
    
    
    MOS = math.floor(MOS) #Redondeo del valor MOS
    cursor.execute('SELECT * FROM Codecs_DataBase where MOS >=' + str(MOS)  +  ' and  MOS <=' + str(MOS+1)  +  ' order by MOS desc')
    records = cursor.fetchall() #Sacar registros

    codecMayor=records[0][0] #Mete en vector el valor del mejor codec.
    print("Códec mayor : ", codecMayor)
    print("sample size : ", records[0][2])
    for row in records:
        print("Códec: ", row[0])
        print("\n")
        
    dlg2.lineEdit.setText(dlg.lineEdit_8.text())
    dlg2.lineEdit.setReadOnly(True)
    

########################################################################### 
####################### Trabajo con la base de datos ######################

conn = sql.connect('PruebaDB.db')
data = pd.read_sql('SELECT MOS FROM Codecs_DataBase', conn)
#print(data)
cursor = conn.cursor()
tablamos=[]
numero=0
minimo=float("inf")
print(minimo)
print("Connected to SQLite")
MOS=0

sqlite_select_query = """SELECT * from Codecs_DataBase"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
print("El total de filas es:  ", len(records))
print("Imprimiendo filas")
for row in records:
    # print("Códec: ", row[0])
    # print("Bit Rate(kbps): ", row[1]) 
    # print("Sample size(B): ", row[2])
    # print("SampleInterval(ms): ", row[3])
    # print("MOS: ", row[4])
    tablamos.append(row[4])
    # print("VPS(ms): ", row[5])
    # print("BW MP: ", row[6])
    # print("BW w/cTTP MP: ", row[7])
    # print("BW Ethernet(kbps): ", row[8])
    # print("PPS: ", row[9])
    # print("\n")

    cursor.close()
    

# for elemento in tablamos:
#     if(elemento>MOS):
#         diferencia=elemento-MOS
#         print('diferencia',diferencia)
#         if(diferencia<minimo and diferencia>=0):
#             minimo=diferencia
#             indice=tablamos.index(elemento)
#             mejorMos=tablamos[indice]
#             print(mejorMos)

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
