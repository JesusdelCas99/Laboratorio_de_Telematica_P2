# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:00:46 2020

@author: SoftLabs
"""

#Importamos libreria para obtener la fecha actual
import calendar
import time
from datetime import datetime, timedelta, date

from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import *

#Importamos modulos para openSaveDialog
import sys
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QFileDialog,QWidget,QPushButton,QHBoxLayout,QVBoxLayout
from PyQt5.uic import loadUi


#Importamos modulos para computo cientifico
import numpy as np

#Importamos las liberías pertinentes para el trabajo con la base de datos
import sqlite3 as sql
import pandas as pd

#Importamos el modulo 'funciones.py' diseñadas
from Funciones import *


########################################################################### 

def Comprobaciones():
    #En esta función se comprueba que todos los parámetros introducidos por el usuario
    #tienen sentido.
    
    Comprobacion=1 #Inicializo para el caso de que no haya ningún error
    
    if dlg.lineEdit.text().isdigit():
        pass
    else:
        ShowMessage("Las empresas clientes debe ser un número entero.","Parámetros incorrectos")
        Comprobacion=0
        
    if dlg.lineEdit_2.text().isdigit():
        pass
    else:
        ShowMessage("Las líneas por cliente debe ser un número entero.","Parámetros incorrectos")
        Comprobacion=0
        
    if dlg.lineEdit_4.text().isdigit():
        pass
    else:
        ShowMessage("Los minutos por llamada deben ser un número entero.","Parámetros incorrectos")
        Comprobacion=0
    
    if isProb(dlg.lineEdit_5.text()):
        pass
    else:
        ShowMessage("La probabilidad de llamada debe ser un número entre 0 y 1.","Parámetros incorrectos")
        Comprobacion=0
        
    if isFloat(dlg.lineEdit_7.text()):
        pass
    else:
        ShowMessage("El ancho de banda de reserva debe ser un número.","Parámetros incorrectos")
        Comprobacion=0
        
    if isFloat(dlg.lineEdit_3.text()):
        pass
    else:
        ShowMessage("El ancho de banda del enlace SIPTRUNK debe ser un número.","Parámetros incorrectos")
        Comprobacion=0
    
    if isProb(dlg.lineEdit_9.text()):
        pass
    else:
        ShowMessage("La probabilidad de bloqueo debe ser un número entre 0 y 1.","Parámetros incorrectos")
        Comprobacion=0
     
    if dlg.lineEdit_11.text().isdigit():
        pass
    else:
        ShowMessage("El retardo de red debe ser un número entero.","Parámetros incorrectos")
        Comprobacion=0
        
    if dlg.lineEdit_10.text().isdigit():
        pass
    else:
        ShowMessage("El Jitter debe ser un número entero.","Parámetros incorrectos")
        Comprobacion=0
    
    
    return Comprobacion

   

def ShowMessage(Details,Fallo):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Error")
    msg.setInformativeText(Fallo)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.setDetailedText(Details)
    msg.exec_()



def CrearArchivo(Ruta_archivo):
    
    if Ruta_archivo=='':
        pass
    
    else:
        print("Creando archivo")
        archivo = open (Ruta_archivo,"a") 
        
    
         # Variable de fecha de hoy
        today = datetime.now()
    
        # Fecha en la q se genera el archivo
        archivo.write("\n" +"El archivo se ha creado: " +  str(datetime.now()) + "\n")
    
        
        return archivo
    
def GuardarDatos(textoArchivo, ruta_creada):
    
    archivo = open (ruta_creada,"a")
    
    archivo.write(textoArchivo)
    
    archivo.close()
    

def V_Paso1():
    
    texto_Codec=dlg.comboBox_5.currentText()
    
    #En caso de seleccionar la opcion de IPESEC, mostrar la opcion de elegir
    #la longitud de cabecera entre los valores teoricos posibles (50-57 Bytes)
    
    if texto_Codec=="IPSEC":
        dlg.spinBox.setVisible(True)
        dlg.label_9.setVisible(True)
    else:
        dlg.spinBox.setVisible(False)
        dlg.label_9.setVisible(False)
    
def V_Paso3():
    
    texto_Codec=dlg3.comboBox.currentText()
    index = Codecs.index(texto_Codec)
    
    dlg3.lineEdit_2.setText(str(1e3*R_final[index]).lstrip('[').rstrip(']') + " ms")
    dlg3.lineEdit_2.setReadOnly(True)
    
    
def V_Paso6():
    #Optimización
    
    global Codecs
    global Codecs_parametros
    
    Codecs=[]
            
    texto_Codec=dlg6.comboBox.currentText()
    index = TodosCodecs.index(texto_Codec)
    
    Codecs.append(texto_Codec)
    
   
    Codecs_parametros[0][:]=TodosCodecs_parametros[index][:]
    

def Codec_Show():
    
    global indexCodec
    
    #Asignamos un valor inicial a esta variable, tal que si es '0' cumple,
    #y si no, no cumple    
    Nocumple=0
    
    texto_Codec=dlg5.comboBox.currentText()
    index = Codecs.index(texto_Codec)
    
    indexCodec = index
    
    
    dlg5.lineEdit.setText(Codecs[index])
    dlg5.lineEdit.setReadOnly(True)
    
    #Mostramos por pantalla el MOS del primer Codec en cuestion
    dlg5.lineEdit_6.setText(str(Codecs_parametros[index][3]))
    dlg5.lineEdit_6.setReadOnly(True) 
    
    if Codecs_parametros[index][3]<MOS:
        dlg5.lineEdit_2.setText("No cumple")
        Nocumple=1
    else:
        dlg5.lineEdit_2.setText("Cumple")
    dlg5.lineEdit_2.setReadOnly(True)
    
    
    if R_final[index]>Retardo_total:
        dlg5.lineEdit_3.setText("No cumple")
        Nocumple=1
    else:
        dlg5.lineEdit_3.setText("Cumple")
    dlg5.lineEdit_3.setReadOnly(True)
    
    
    #Tal y como está planteado no se me ocurre forma de que se supere la
    #probabilidad de bloqueo que introduce el usuario
    dlg5.lineEdit_4.setText("Cumple")
    dlg5.lineEdit_4.setReadOnly(True)        
    
    
    if BW_SP[index] > Bandwidth:
        dlg5.lineEdit_5.setText("No cumple")
        Nocumple=1
    else:
        dlg5.lineEdit_5.setText("Cumple")
    dlg5.lineEdit_5.setReadOnly(True)
        

    if Nocumple == 1:
        
        dlg5.pushButton.setVisible(False)
        dlg5.line_7.setVisible(True)
        dlg5.line_4.setVisible(True)
        dlg5.line_9.setVisible(True)
        dlg5.line_8.setVisible(True)
        dlg5.label_7.setVisible(True)
        dlg5.label_6.setVisible(True)
        dlg5.pushButton_2.setVisible(True)
        dlg5.pushButton_3.setVisible(True)
        dlg5.frame_3.setVisible(True)
        
    else:
        #Hacemos invisible la ventana de aviso de que el Codec no cumple
        dlg5.line_7.setVisible(False)
        dlg5.line_4.setVisible(False)
        dlg5.line_9.setVisible(False)
        dlg5.line_8.setVisible(False)
        dlg5.label_7.setVisible(False)
        dlg5.label_6.setVisible(False)
        dlg5.pushButton_2.setVisible(False)
        dlg5.pushButton_3.setVisible(False)
        dlg5.frame_3.setVisible(False)
        dlg5.pushButton.setVisible(True)


    

def Paso0():
    
    dlg5.close()
    dlg6.close()
    dlg.show()
    

def Paso2(): 
    
    global textoArchivo
    global textoArchivo_def
    
    dlg2.comboBox.clear()
    
       
    
    global Codecs_parametros
    global Codecs
    global MOS
    global dim
    
    textoArchivo_def = ""
    
    
    MOS=dlg.comboBox_2.currentText()

    
    if MOS=='Excelente':
        MOS=5
    elif MOS=='Bueno':
        MOS=4
    elif MOS=='Aceptable':
        MOS=3
    elif MOS=='Bajo':
        MOS=2
    else:
        MOS=1

    #Seleccionamos de la base de datos los codecs que tengan MOS que satisfaga 
    #el QoE introducido por el usuario
    conn = sql.connect('DataBase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Codecs_DataBase where MOS >=' + str(MOS))
    records = cursor.fetchall()
    
    
    Codecs_parametros=np.zeros((len(records),10))
    Codecs=list()
    
    #Agrupo todos los codecs en una lista y sus parámetros en una matriz
    z=0
    
    for raw in records:        
          Codecs.append(raw[0])
          for j in range(1,11):             
              Codecs_parametros[z,j-1]=float(raw[j])
              
          z+=1
    
    dim=len(Codecs_parametros)
    
    if dim==0:
        ShowMessage("Ningún Codec cumple QoS excelente.", None)
    elif (dim !=0) & Comprobaciones():        
        dlg_aviso.close() #Cerramos la pestaña de avisos en caso de que estuviese abierta
        dlg.close() #Cerramos la ventana principal
        dlg2.show() #Abrimos la ventana que nos proporciona los datos del paso 2
        
        
    for i in range(dim):   
        dlg2.comboBox.addItem(Codecs[i])
               
              
    dlg2.lineEdit.setText(dlg.comboBox_2.currentText())
    dlg2.lineEdit.setReadOnly(True)  
        
    
    
##########################################################################

def Paso3():
    
    
    global Retardo_total
    global R_final
    global dim #Numero de Codecs seleccionados
    
    #Definimos variables globales para poder mostrarlas en el texto
    global textoArchivo_def
    global Jitter 
    global Retardo_red
    global Retardo_VoIp
    global Retardo_G114
    global n_look_ahead
    global VPS
    global R_fin1
    global R_fin2
    global texto_r_final
    global texto_r_final_v
       
    
    Jitter=float(dlg.lineEdit_11.text())*1e-3
    
    Retardo_red=float(dlg.lineEdit_10.text())*1e-3
    
    Retardo_VoIp=dlg.comboBox.currentText()
    
    Retardo_G114=dlg.comboBox_3.currentText()
    
    
                       
    if Retardo_VoIp=='Aceptable':
        Retardo_VoIp=150*1e-3
    elif Retardo_VoIp=='Moderado':
        Retardo_VoIp=400*1e-3
    else:
        Retardo_VoIp=1
        
        
    
    if Retardo_G114=='Muy satisfecho':
        Retardo_G114=200*1e-3
    elif Retardo_G114=='Satisfecho':
        Retardo_G114=287.5*1e-3
    elif Retardo_G114=='Alguno insatisfecho':
        Retardo_G114=387.5*1e-3
    elif Retardo_G114=='Mucho insatisfecho':
        Retardo_G114=550*1e-3
    elif Retardo_G114=='Casi todos insatisfechos':
        Retardo_G114=1
        
                
    #Mostramos la ventana referente al paso 3
    dlg2.close()
    dlg3.show() 
    
    dlg3.comboBox.clear()
    
    dlg3.comboBox.addItems(Codecs)
    
    
    dlg3.lineEdit_11.setText(dlg.lineEdit_11.text() + " ms")
    dlg3.lineEdit_11.setReadOnly(True) 
    
    dlg3.lineEdit_10.setText(dlg.lineEdit_10.text() + " ms")
    dlg3.lineEdit_10.setReadOnly(True) 
    
    dlg3.lineEdit_12.setText(str(Retardo_G114*1e3) + " ms")
    dlg3.lineEdit_12.setReadOnly(True)
    
    dlg3.lineEdit_13.setText(str(Retardo_VoIp*1e3) + " ms")
    dlg3.lineEdit_13.setReadOnly(True)
    
    
    
    Retardo_total=min(Retardo_G114,Retardo_VoIp)
    
    #En los retardos de origen no consideramos los de señalizacion
    #Introducimos el efecto de pipelining en el retardo
    
    dim=len(Codecs_parametros)
    
    
    #Inicializamos vector para el retardo total acumulado
    R_final=np.zeros((dim,1))
    
    #Inicializamos vector para el numero de paquetes del buffer antijitter
    Storage_P=np.zeros((dim,1))
    
    texto_r_final_v = ["" for x in range(dim)]
    
    # texto_r_final=""
    #Calculo del retardo total (Origen+Red+Destino)
    for i in range(dim):
        
        #Cargamos el retardo de look ahead de la base de datos
        n_look_ahead=Codecs_parametros[i][9]*1e-3
        
        #Retraso de paquetizacion
        VPS=8*Codecs_parametros[i][4]/((Codecs_parametros[i][0])*1e3)
        R_final[i]=VPS
        
        texto_r_final = ""
        
        texto_r_final += "Codec Bit-Rate: " + str(Codecs_parametros[i][0]) + "kbps \n"
        
        texto_r_final += "\nRetraso paquetizacion: " + str(1e3*R_final[i])+ " ms \n"
        
        #Retraso algoritmico
        R_final[i]=R_final[i]+n_look_ahead
        Retraso_algoritmico=R_final[i]
        
        texto_r_final += "Retraso algoritmico: " + str(1e3*R_final[i])+ " ms \n"
        
        #Tiempo de ejecucion de la compresion. Consideramos un 10% de CSI
        #por trama
        R_final[i]=R_final[i]+0.1*Codecs_parametros[i][2]*1e-3
        
        texto_r_final += "Tiempo ejecucion de la compresion: " + str(1e3*R_final[i])+" ms\n"
        
        #Añadimos el retardo de red
        R_final[i]=R_final[i]+Retardo_red
        
        texto_r_final += "Añadimos retardo de red: " + str(1e3*R_final[i])+" ms\n"
        #Retardo de decodificacion
        R_final[i]=R_final[i]+0.1*Codecs_parametros[i][2]*1e-3
        texto_r_final += "Retardo de decodificacion: " + str(1e3*R_final[i])+" ms\n"
        
        
        
        #Retardo de buffer antijitter. Escogemos un numero entero de posibles
        #paquetes en el buffer
        R_fin1=int((1.5*Jitter)/VPS)*VPS+R_final[i]
        R_fin2=int((2*Jitter)/VPS)*VPS+R_final[i]
        
        
        #En caso de obtener para los dos tamaños de buffer antijitter un 
        #retardo que entre dentro de las cotas, escogemos el que tenga mayor
        #tamaño de buffer antijitter
        if R_fin2<Retardo_total:
            R_final[i]=R_fin2
            
            #Numero de paquetes a almacenar por el buffer antijitter
            Storage_P[i]=int((2*Jitter)/VPS)
            texto_r_final += "Nº paquetes en el buffer anti-jitter: " + str(int(Storage_P[i]))+"\n"
        else:
            R_final[i]=R_fin1
            
            #Numero de paquetes a almacenar por el buffer antijitter
            Storage_P[i]=int((1.5*Jitter)/VPS)
            texto_r_final += "Nº paquetes en el buffer anti-jitter: " + str(int(Storage_P[i]))+"\n"
    
        texto_r_final_v[i] = texto_r_final
    
        
    dlg3.lineEdit_2.setText(str(1e3*R_final[0]).lstrip('[').rstrip(']') + " ms")
    dlg3.lineEdit_2.setReadOnly(True)
    
    
    dlg3.comboBox.activated.connect(V_Paso3) 
           
                                         
# Calculo de GoS número de líneas en una ventana adicional #################
def Paso4():
    
    global Nc
    global NI
    global Tpll
    global Pll
    global BHT

 
    #Mostramos la ventana referente al paso 4
    dlg3.close()
    dlg4.show()    
    
    dlg4.lineEdit_2.setText(dlg.lineEdit_9.text()) 
    dlg4.lineEdit_2.setReadOnly(True)
    
    #Definimos el numero de lineas como variable global
    global N_lineas
    

    #Cargamos los parametros como variables flotantes para su tratamiento 
    #matematico
    Nc=float(dlg.lineEdit.text())
    NI=float(dlg.lineEdit_2.text())
    Tpll=float(dlg.lineEdit_4.text())
    Pll=float(dlg.lineEdit_5.text())
    
    #Calculamos el Busy Hour Traffic
    BHT=(Nc*NI*Tpll*Pll)/60
    
    dlg4.TraficoBHT.setText(str(BHT) + " Erlangs")
    dlg4.TraficoBHT.setReadOnly(True)
    
    #Calculamos el numero de lineas en base a la funcion Erlang_B2 para el 
    #primer Codec de la lista
    N_lineas=Erlang_B2(BHT,float(dlg.lineEdit_9.text()))
    
    dlg4.lineEdit_3.setText(str(N_lineas))
    dlg4.lineEdit_3.setReadOnly(True) 
    
        

def Paso5():
    
#Defino variables globales para mostrar en el texto
    global B_W_percentage
    global P_Tuneles
    global P_Enlace
    global L_RTP_Cabeceras
    global L_RTP
    global PPS
    global Bw_llamada
    global BW_SP_RTP
    global L_cRTP_Cabeceras
    global L_cRTP
    global BW_SP_cRTP

    global BW_SP
    
    global L_RTP_vector
    global PPS_vector
    global BW_SP_RTP_vector
    global L_cRTP_vector
    global Bw_llamada_vector
    global BW_SP_cRTP_vector
    

    
    #Mostramos la ventana referente al paso 5
    dlg4.close()
    dlg5.show()
    
    
    dlg5.pushButton_2.hide()
    dlg5.pushButton_3.hide()
    dlg5.label_6.hide()
    dlg5.label_7.hide()
    
    
    #Colocamos el ancho de banda con variable global
    global Bandwidth
    
    #Variable para controlar si es necesario Paso6
    Nocumple=0
    
    
    #Calculamos el ancho de banda global
    Bandwidth=(float(dlg.lineEdit_3.text()))*1e6
    
    #Extraemos de la GUI los parametros de cabeceras del paquete
    P_Enlace=dlg.comboBox_4.currentText()
    
    P_Tuneles=dlg.comboBox_5.currentText()
    
    B_W_percentage=float(dlg.lineEdit_7.text()) 
                             
  
    
    if P_Tuneles=='MPLS':
        P_Tuneles=4
    elif P_Tuneles=='L2TP':
        P_Tuneles=24
    elif P_Tuneles=='IPSEC':
        P_Tuneles=float(dlg.spinBox.text())
    else:
        P_Tuneles=0
        
        
    if P_Enlace=='Ethernet 802.1q':
        P_Enlace=20
    elif P_Enlace=='Ethernet q-inq':
        P_Enlace=22
    elif P_Enlace=='PPP':
        P_Enlace=6
    elif P_Enlace=='PPOE':
        P_Enlace=24
    elif P_Enlace=='Ethernet': 
        P_Enlace=18
        
        
    #Calculamos la longitud de la cabecera para RTP y cRTP que sera 
    #la misma para todos los Codecs. Para el caso de cRTP consideramos
    #que comprime IP/UDP/RTP a un total de 4B. Las colas asociadas al checksum
    #siguen presentes en cRTP
    L_RTP_Cabeceras=int(P_Enlace) + int(P_Tuneles) + 20 + 8 + 12 + 4
    L_cRTP_Cabeceras=int(P_Enlace) + int(P_Tuneles) + 4 + 4
    
    #Calculamos el ancho de banda para los dos posibles casos: RTP y cRTP
    #CASO 1: RTP: Tendremos en cuenta el checksum (4bytes)
    BW_SP=np.zeros((dim,1))
    
    L_RTP_vector=np.zeros((dim,1))
    PPS_vector=np.zeros((dim,1))
    BW_SP_RTP_vector=np.zeros((dim,1))
    L_cRTP_vector=np.zeros((dim,1))
    Bw_llamada_vector=np.zeros((dim,1))
    BW_SP_cRTP_vector=np.zeros((dim,1))
    
    
    
    #Reseteamos el comBox
    dlg5.comboBox.clear()
    
    for i in range(dim):
        
        L_RTP=8*(Codecs_parametros[i][4]+L_RTP_Cabeceras)
        L_RTP_vector[i]=L_RTP
        PPS=(Codecs_parametros[i][0]*1e3)/(8*Codecs_parametros[i][4])
        PPS_vector[i]=PPS
        Bw_llamada=L_RTP*PPS*(1+B_W_percentage)
        BW_SP_RTP=N_lineas*Bw_llamada
        BW_SP_RTP_vector[i]=BW_SP_RTP 
        
        L_cRTP=8*(Codecs_parametros[i][4]+L_cRTP_Cabeceras)
        L_cRTP_vector[i]=L_cRTP
        Bw_llamada=L_cRTP*PPS*(1+B_W_percentage)
        Bw_llamada_vector[i]=Bw_llamada
        BW_SP_cRTP=N_lineas*Bw_llamada
        BW_SP_cRTP_vector[i]=BW_SP_cRTP
        
        #Nos quedaremos con el ancho de banda que se encuentre por debajo
        #del establecido por el cliente para el SIP Trunk. En caso de que 
        #ambos se encuentren por debajo nos quedaremos con el que use RTP, 
        #desechando el usado con cRTP
        
        #Puede ocurrir que ninguno de los dos se encuentre fuera del 
        #limite, pero esa opcion la filtraremos mas adelante (no ahora). 
        #Por ahora nos limitamos a quedarnos con la mejor opcion
        if BW_SP_RTP<=Bandwidth:
            BW_SP[i]=BW_SP_RTP #Nos quedamos con RTP
        else:
            BW_SP[i]=BW_SP_cRTP #Nos quedamos con cRTP
        
        dlg5.comboBox.addItem(Codecs[i])
            
    #adding action to combo box 
    dlg5.comboBox.activated.connect(Codec_Show)       
    
    dlg5.lineEdit.setText(Codecs[0])
    dlg5.lineEdit.setReadOnly(True)
    
    
    if Codecs_parametros[0][3]<MOS:
        dlg5.lineEdit_2.setText("No cumple")
        Nocumple=1
    else:
        dlg5.lineEdit_2.setText("Cumple")
    dlg5.lineEdit_2.setReadOnly(True)
    
    
    if R_final[0]>Retardo_total:
        dlg5.lineEdit_3.setText("No cumple")
        Nocumple=1
    else:
        dlg5.lineEdit_3.setText("Cumple")
    dlg5.lineEdit_3.setReadOnly(True)
    
    
    #Tal y como está planteado no se me ocurre forma de que se supere la
    #probabilidad de bloqueo que introduce el usuario
    dlg5.lineEdit_4.setText("Cumple")
    dlg5.lineEdit_4.setReadOnly(True)  

    #Mostramos por pantalla el MOS del primer Codec en cuestion
    dlg5.lineEdit_6.setText(str(Codecs_parametros[0][3]))
    dlg5.lineEdit_6.setReadOnly(True) 
        
    
    if BW_SP[0] > Bandwidth:
        dlg5.lineEdit_5.setText("No cumple")
        Nocumple=1
    else:
        dlg5.lineEdit_5.setText("Cumple")
    dlg5.lineEdit_5.setReadOnly(True)
        

    if Nocumple == 1:

        dlg5.pushButton.setVisible(False)
        dlg5.line_7.setVisible(True)
        dlg5.line_4.setVisible(True)
        dlg5.line_9.setVisible(True)
        dlg5.line_8.setVisible(True)
        dlg5.label_7.setVisible(True)
        dlg5.label_6.setVisible(True)
        dlg5.pushButton_2.setVisible(True)
        dlg5.pushButton_3.setVisible(True)
        dlg5.frame_3.setVisible(True)
    else:
        
        #Hacemos invisible la ventana de aviso de que el Codec no cumple
        dlg5.line_7.setVisible(False)
        dlg5.line_4.setVisible(False)
        dlg5.line_9.setVisible(False)
        dlg5.line_8.setVisible(False)
        dlg5.label_7.setVisible(False)
        dlg5.label_6.setVisible(False)
        dlg5.pushButton_2.setVisible(False)
        dlg5.pushButton_3.setVisible(False)
        dlg5.frame_3.setVisible(False)
        dlg5.pushButton.setVisible(True)
        
        
    

def Paso6():
    
    dlg5.close()
    dlg6.show()
    
    global TodosCodecs_parametros
    global TodosCodecs
    global Codecs
    global Codecs_parametros
    
    
    Codecs_parametros = np.zeros((1,10))
    
    conn = sql.connect('DataBase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Codecs_DataBase where MOS >=' + str(0))
    records = cursor.fetchall()
    
    
    TodosCodecs_parametros=np.zeros((len(records),10))
    TodosCodecs=list()
    dim=1
        
    
    #Agrupo todos los codecs en una lista y sus parámetros en una matriz
    z=0
    
    for raw in records:        
          TodosCodecs.append(raw[0])
          for j in range(1,11):             
              TodosCodecs_parametros[z,j-1]=float(raw[j])
          z+=1
    
    
    dlg6.comboBox.clear()
    dlg6.comboBox.addItems(TodosCodecs)
    
    Codecs=[]
            
    texto_Codec=dlg6.comboBox.currentText()
    index = TodosCodecs.index(texto_Codec)
    
    Codecs.append(texto_Codec)
    
   
    Codecs_parametros[0][:]=TodosCodecs_parametros[index][:]
    
    #Activamos el evento
    dlg6.comboBox.activated.connect(V_Paso6)
       

def Paso7():
    
    global textoArchivo
    #global indiceCodec
        
    textoArchivo = ""
    textoArchivo += "\n===============Paso 2===============\n"
        
    textoArchivo += "\n---Parametros de entrada QoE---\n"
    textoArchivo += "MOS: " + str(MOS) + "\n"
        
    textoArchivo += "\n---Codecs validos---\n"
        
    for codec in Codecs:        
          textoArchivo += str(codec) + "\n"
        
    textoArchivo += "\n===============Paso 3===============\n"
    
    textoArchivo += "\n---Parametros de entrada QoS----\n\n"
        
    textoArchivo += "Jitter: " + str(1e3*Jitter) + " ms\n"
    textoArchivo += "Retardo red: " + str(1e3*Retardo_red) + " ms\n"
    textoArchivo += "Retardo VoIp: " + str(1e3*Retardo_VoIp) + " ms\n"
    textoArchivo += "Retardo G114: " + str(1e3*Retardo_G114) + " ms\n"
        
    textoArchivo += "\n---Resultados parciales---\n\n"
        
    textoArchivo += "Retardo total: " + str(Retardo_total) + " s\n"
    textoArchivo += "Retardo look_ahead: " + str(1e3*n_look_ahead) + " ms\n"
    textoArchivo += "VPS: " + str(1e3*VPS) + " ms\n" 
    
    indiceCodec = 0
    
    try:
        indiceCodec = indexCodec
    except:
        indiceCodec = 0
    
    textoArchivo += "\nPara codec: " + str(Codecs[indiceCodec])+ "\n\n"
    textoArchivo += texto_r_final_v[indiceCodec] 



    textoArchivo += "\n===============Paso 4===============\n"
        
    textoArchivo += "\n---Parametros de entrada ----\n\n"
        
    textoArchivo += "Numero clientes: " + str(int(Nc)) + "\n"
    textoArchivo += "Numero lineas: " + str(int(NI)) + "\n"
    textoArchivo += "Tiempo medio llamada: " + str(Tpll) + " min\n"
    textoArchivo += "Probabilidad llamada: " + str(Pll) + "\n"
        
        
    textoArchivo += "\n---Resultados parciales---\n\n"
        
    textoArchivo += "Busy Hour Traffic: " + str(BHT) + " Erlang\n"
    textoArchivo += "Numero de lineas: " + str(int(N_lineas)) + "\n"
    
    
    textoArchivo += "\n===============Paso 5===============\n"
        
    textoArchivo += "\n---Parametros de entrada ----\n\n"
        
    textoArchivo += "Ancho de banda SIPTRUNK: " + str(1e-6*Bandwidth) + " Mbps\n"
    textoArchivo += "Ancho de banda de reserva: " + str(B_W_percentage) + " % del SIPTRUNK\n"
    textoArchivo += "Cabecera para túneles:  " + str(P_Tuneles) + " Bytes\n"
    textoArchivo += "Cabecera de enlace: " + str(P_Enlace) + " Bytes\n"
        
    textoArchivo += "\n---Resultados Parciales ----\n\n"
    
    textoArchivo += "Tamaño cabecera RTP:  " + str(L_RTP_Cabeceras) + " Bytes\n"
    textoArchivo += "Tamaño cabecera cRTP: " + str(L_cRTP_Cabeceras) + " Bytes\n\n"
    

    
    
    textoArchivo += "\nPara codec: " + str(Codecs[indiceCodec])+ "\n\n"
    textoArchivo += "Longitud total (RTP):  " + str(L_RTP_vector[indiceCodec]) + " Bytes\n"
    textoArchivo += "PPS: " + str(PPS_vector[indiceCodec]) + "\n"
    textoArchivo += "Ancho de banda total RTP: " + str(1e-6*BW_SP_RTP_vector[indiceCodec]) + " Mbps\n"
    textoArchivo += "Longitud total (cRTP): " + str(L_cRTP_vector[indiceCodec]) + " Bytes\n"
    textoArchivo += "Ancho de banda total cRTP: " + str(1e-6*BW_SP_cRTP_vector[indiceCodec]) + " Mbps\n"
    
    if BW_SP_RTP<=Bandwidth:
        textoArchivo += "Nos quedamos con RTP, BW_SP: " + str(1e-6*BW_SP[indiceCodec]) + " Mbps\n\n"
    else:
        textoArchivo += "Nos quedamos con cRTP, BW_SP: " + str(1e-6*BW_SP[indiceCodec]) +" Mbps\n"
     
        
    textoArchivo += "\n========================================"
    

def openSaveDialog():
    
   global textoArchivo
   global ruta_creada
    
   option=QFileDialog.Options()
   option|=QFileDialog.DontUseNativeDialog
    
    
   file=QFileDialog.getSaveFileName(widget)
   ruta_creada=file[0]
   CrearArchivo(file[0])
   
   Paso7()
   if ruta_creada=='':
       pass
   else:
       GuardarDatos(textoArchivo, ruta_creada) 
       

 
           
###########################################################################
################## PROGRAMACION BACK-END ##################################
###########################################################################

                            
app=QtWidgets.QApplication([])


#Cargamos el archivo '.ui' diseñado mediante Qt Designer
dlg=uic.loadUi("VoIp_SoftLab.ui")

dlg.spinBox.setVisible(False)
dlg.label_9.setVisible(False)
    
dlg2=uic.loadUi("Paso2.ui")
dlg3=uic.loadUi("Paso3.ui")
dlg4=uic.loadUi("Paso4.ui")
dlg5=uic.loadUi("Paso5.ui")
dlg6=uic.loadUi("Paso6a.ui")
dlg_aviso=uic.loadUi("Aviso.ui")


#Placeholders, ¿usar en otros campos?
dlg.lineEdit_5.setPlaceholderText("Probabilidad entre 0-1")
dlg.lineEdit_9.setPlaceholderText("0-1")


#Activamos el evento referente a la cabecera IPESEC 
dlg.comboBox_5.activated.connect(V_Paso1) 

#Botones en las distintas ventanas que dan paso a una nueva.

dlg.pushButton.clicked.connect(Paso2) 

dlg2.pushButton.clicked.connect(Paso3)


dlg3.pushButton.clicked.connect(Paso4)


dlg4.pushButton.clicked.connect(Paso5)


dlg5.pushButton_3.clicked.connect(Paso0)


dlg5.pushButton_2.clicked.connect(Paso6)


dlg5.pushButton.clicked.connect(openSaveDialog)


dlg6.pushButton.clicked.connect(Paso3)


# dlg7.pushButton.clicked.connect(Paso7)

dlg5.pushButton.clicked.connect(Paso7)


mainWindow=QMainWindow()
widget=QWidget()

# dlg7.pushButton2.clicked.connect(openSaveDialog)


dlg.show()
app.exec()

#https://www.tutorialspoint.com/pyqt/pyqt_qfiledialog_widget.htm