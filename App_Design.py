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

#Importamos modulos para computo cientifico
import numpy as np

#Importamos las liberías pertinentes para el trabajo con la base de datos
import sqlite3 as sql
import pandas as pd

#Importamos el modulo 'funciones.py' diseñadas
from Funciones import *


########################################################################### 
def CrearArchivo(Ruta_archivo):
    
    print("Creando archivo")
    archivo = open (Ruta_archivo,"a") 
    

     # Variable de fecha de hoy
    today = datetime.now()

    # Fecha en la q se genera el archivo
    archivo.write("\n" +"El archivo se ha creado: " +  str(datetime.now()) + "\n")

    
    return archivo
    
def GuardarDatos(textoArchivo, Ruta_archivo):
    
    # print("aBRIENDO ARCHIVO " + Ruta_archivo)
    
    archivo = open (Ruta_archivo,"a")
    
      # Variable de fecha de hoy
    today = datetime.now()

    # Fecha en la q se genera el archivo
    # archivo.write("\n" +"los datos se han guardado: " + str(datetime.now()) + "\n")
    
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
    

def Codec_Show():
    
    global textoArchivo_def
    
    #Asignamos un valor inicial a esta variable, tal que si es '0' cumple,
    #y si no, no cumple    
    Nocumple=0
    
    texto_Codec=dlg5.comboBox.currentText()
    index = Codecs.index(texto_Codec)
    
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

    
    textoArchivo_def += textoArchivo
    

def Paso0():
    
    dlg5.close()
    dlg.show()


def Paso2(): 
    
    global textoArchivo
    
    textoArchivo = ""
    textoArchivo += "\n===============Paso 2===============\n"
    textoArchivo += "\n---Parametros de entrada QoE---\n"
       
    
    global Codecs_parametros
    global Codecs
    global MOS
    global textoArchivo_def
    global dim
    
    textoArchivo_def = ""
    
    
    MOS=dlg.comboBox_2.currentText()
    textoArchivo += "MOS=" + str(MOS) + "\n"
    
    if MOS=='Excelente':
        MOS=5
        textoArchivo += "MOS=" + str(MOS) + "\n"
    elif MOS=='Bueno':
        MOS=4
        textoArchivo += "MOS=" + str(MOS) + "\n"
    elif MOS=='Aceptable':
        MOS=3
        textoArchivo += "MOS=" + str(MOS) + "\n"
    elif MOS=='Bajo':
        MOS=2
        textoArchivo += "MOS=" + str(MOS) + "\n"
    else:
        MOS=1
        textoArchivo += "MOS=" + str(MOS) + "\n"

    #Seleccionamos de la base de datos los codecs que tengan MOS que satisfaga 
    #el QoE introducido por el usuario
    conn = sql.connect('DataBase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Codecs_DataBase where MOS >=' + str(MOS))
    records = cursor.fetchall()
    
    textoArchivo += "\n---Codecs validos---\n"
    
    Codecs_parametros=np.zeros((len(records),10))
    Codecs=list()
    
    #Agrupo todos los codecs en una lista y sus parámetros en una matriz
    z=0
    
    for raw in records:        
          Codecs.append(raw[0])
          for j in range(1,11):             
              Codecs_parametros[z,j-1]=float(raw[j])
              
          print("codec",Codecs_parametros[z])   
          
          print("Codecs validos",raw[0]) 
          textoArchivo +=  str(raw[0]) + "\n"
          z+=1
    
    dim=len(Codecs_parametros)
    
    if dim==0:
        dlg_aviso.show()
    else:
        
        dlg_aviso.close() #Cerramos la pestaña de avisos en caso de que estuviese abierta
        dlg.close() #Cerramos la ventana principal
        dlg2.show() #Abrimos la ventana que nos proporciona los datos del paso 2
        
        
    for i in range(dim):   
        dlg2.comboBox.addItem(Codecs[i])
               
              
    dlg2.lineEdit.setText(dlg.comboBox_2.currentText())
    dlg2.lineEdit.setReadOnly(True)  
        
        
    textoArchivo_def += textoArchivo
    
    
##########################################################################

def Paso3():
    
    
    global Retardo_total
    global R_final
    global dim #Numero de Codecs seleccionados
    global textoArchivo_def
    
    
    textoArchivo = ""
    textoArchivo += "\n===============Paso 3===============\n"
    
    textoArchivo += "\n---Parametros de entrada QoS----\n\n"
    
    
    Jitter=float(dlg.lineEdit_11.text())*1e-3
    textoArchivo += "Jitter=" + str(Jitter) + "\n"
    
    Retardo_red=float(dlg.lineEdit_10.text())*1e-3
    textoArchivo += "Retardo_red=" + str(Retardo_red) + "\n"
    
    Retardo_VoIp=dlg.comboBox.currentText()
    
    Retardo_G114=dlg.comboBox_3.currentText()
    
    
                       
    if Retardo_VoIp=='Aceptable':
        textoArchivo += "Retardo_VoIp=" + str(Retardo_VoIp) + "\n"
        Retardo_VoIp=150*1e-3
        textoArchivo += "Retardo_VoIp=" + str(Retardo_VoIp) + "\n"
    elif Retardo_VoIp=='Moderado':
        textoArchivo += "Retardo_VoIp=" + str(Retardo_VoIp) + "\n"
        Retardo_VoIp=400*1e-3
        textoArchivo += "Retardo_VoIp=" + str(Retardo_VoIp) + "\n"
    else:
        Retardo_VoIp=1
        textoArchivo += "Retardo_VoIp=" + str(Retardo_VoIp) + "\n"
        
        
    
    if Retardo_G114=='Muy satisfecho':
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
        Retardo_G114=200*1e-3
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
    elif Retardo_G114=='Satisfecho':
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
        Retardo_G114=287.5*1e-3
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
    elif Retardo_G114=='Alguno insatisfecho':
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
        Retardo_G114=387.5*1e-3
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
    elif Retardo_G114=='Mucho insatisfecho':
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
        Retardo_G114=550*1e-3
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
    elif Retardo_G114=='Casi todos insatisfechos':
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
        Retardo_G114=1
        textoArchivo += "Retardo_G114=" + str(Retardo_G114) + "\n"
        
                
    #Mostramos la ventana referente al paso 3
    dlg2.close()
    dlg3.show() 
    
    for i in range(dim):
        dlg3.comboBox.addItem(Codecs[i])
    
    
    dlg3.lineEdit_11.setText(dlg.lineEdit_11.text() + " ms")
    dlg3.lineEdit_11.setReadOnly(True) 
    
    dlg3.lineEdit_10.setText(dlg.lineEdit_10.text() + " ms")
    dlg3.lineEdit_10.setReadOnly(True) 
    
    dlg3.lineEdit_12.setText(str(Retardo_G114*1e3) + " ms")
    dlg3.lineEdit_12.setReadOnly(True)
    
    dlg3.lineEdit_13.setText(str(Retardo_VoIp*1e3) + " ms")
    dlg3.lineEdit_13.setReadOnly(True)
    
    
    textoArchivo += "\n---Resultados parciales---\n\n"
    
    Retardo_total=min(Retardo_G114,Retardo_VoIp)
    textoArchivo += "Retardo_total=" + str(Retardo_total) + "\n"
    
    #En los retardos de origen no consideramos los de señalizacion
    #Introducimos el efecto de pipelining en el retardo
    
    dim=len(Codecs_parametros)
    
    
    #Inicializamos vector para el retardo total acumulado
    R_final=np.zeros((dim,1))
    
    #Inicializamos vector para el numero de paquetes del buffer antijitter
    Storage_P=np.zeros((dim,1))
    
    #Calculo del retardo total (Origen+Red+Destino)
    for i in range(dim):
        
        #Cargamos el retardo de look ahead de la base de datos
        n_look_ahead=Codecs_parametros[i][9]*1e-3
        textoArchivo += "\nRetardo_look_ahead=" + str(n_look_ahead) + "\n" 
        
        #Retraso de paquetizacion
        VPS=8*Codecs_parametros[i][4]/((Codecs_parametros[i][0])*1e3)
        textoArchivo += "VPS=" + str(R_final[i]) + "\n" 
        print("VPS",VPS)
        R_final[i]=VPS
        textoArchivo += "Retraso_paquetizacion=" + str(R_final[i]) + "\n" 
        
        #Retraso algoritmico
        R_final[i]=R_final[i]+n_look_ahead
        textoArchivo += "Retraso_algoritmico=" + str(R_final[i]) + "\n" 
        print("Rfinal",R_final[i])
        
        #Tiempo de ejecucion de la compresion. Consideramos un 10% de CSI
        #por trama
        R_final[i]=R_final[i]+0.1*Codecs_parametros[i][2]*1e-3
        textoArchivo += "Consideramos Tiempo_ejecucion =" + str(R_final[i]) + "\n" 
        print("Tejercucion",R_final[i])
        
        #Añadimos el retardo de red
        R_final[i]=R_final[i]+Retardo_red
        textoArchivo += "Añadiendo el retardo de red=" + str(R_final[i]) + "\n" 
        
        
        #Retardo de decodificacion
        R_final[i]=R_final[i]+0.1*Codecs_parametros[i][2]*1e-3
        textoArchivo += "Retardo de red ofrecido=" + str(R_final[i]) + "\n" 
        
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
            textoArchivo += "Numero de paquetes a almacenar=" + str(Storage_P[i]) + "\n" 
        else:
            R_final[i]=R_fin1
            
            #Numero de paquetes a almacenar por el buffer antijitter
            Storage_P[i]=int((1.5*Jitter)/VPS)
            textoArchivo += "Numero de paquetes a almacenar=" + str(Storage_P[i]) + "\n" 
    
    textoArchivo += "VPS=" + str(VPS) + "\n" 
        
    dlg3.lineEdit_2.setText(str(1e3*R_final[0]).lstrip('[').rstrip(']') + " ms")
    dlg3.lineEdit_2.setReadOnly(True)
    
    
    dlg3.comboBox.activated.connect(V_Paso3) 
           
      
    textoArchivo_def += textoArchivo   
                      
           
# Calculo de GoS número de líneas en una ventana adicional #################
def Paso4():
    
    global textoArchivo_def
    # textoArchivo_def = ""
    
    textoArchivo = ""
    textoArchivo += "\n===============Paso 4===============\n"
    #Mostramos la ventana referente al paso 4
    dlg3.close()
    dlg4.show()    
    
    dlg4.lineEdit_2.setText(dlg.lineEdit_9.text()) 
    dlg4.lineEdit_2.setReadOnly(True)
    
    #Definimos el numero de lineas como variable global
    global N_lineas
    
    textoArchivo += "\n---Parametros de entrada ----\n\n"
    #Cargamos los parametros como variables flotantes para su tratamiento 
    #matematico
    Nc=float(dlg.lineEdit.text())
    textoArchivo += "Numero_clientes=" + str(Nc) + "\n"
    NI=float(dlg.lineEdit_2.text())
    textoArchivo += "Numero_lineas=" + str(NI) + "\n"
    Tpll=float(dlg.lineEdit_4.text())
    textoArchivo += "Tiempo_medio_llamada=" + str(Tpll) + "\n"
    Pll=float(dlg.lineEdit_5.text())
    textoArchivo += "Probabilidad_llamada=" + str(Pll) + "\n"
    
    textoArchivo += "\n---Resultados parciales ----\n\n"
    #Calculamos el Busy Hour Traffic
    BHT=(Nc*NI*Tpll*Pll)/60
    textoArchivo += "Busy Hour Traffic=" + str(BHT) + "\n"
    
    dlg4.TraficoBHT.setText(str(BHT) + " Erlangs")
    dlg4.TraficoBHT.setReadOnly(True)
    
    #Calculamos el numero de lineas en base a la funcion Erlang_B2 para el 
    #primer Codec de la lista
    N_lineas=Erlang_B2(BHT,float(dlg.lineEdit_9.text()))
    textoArchivo += "Numero de lineas=" + str(N_lineas) + "\n"
    
    dlg4.lineEdit_3.setText(str(N_lineas))
    dlg4.lineEdit_3.setReadOnly(True) 
    
    
    textoArchivo_def += textoArchivo
    

def Paso5():
    
    global textoArchivo_def
    global BW_SP
    #textoArchivo_def = ""
    
    textoArchivo = ""
    textoArchivo += "\n===============Paso 5===============\n"
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
    
    textoArchivo += "\n---Parametros de entrada ----\n\n"
    
    #Calculamos el ancho de banda global
    Bandwidth=(float(dlg.lineEdit_3.text()))*1e6
    textoArchivo += "Ancho de banda SIPTRUNK=" + str(Bandwidth) + "\n"
    
    #Extraemos de la GUI los parametros de cabeceras del paquete
    P_Enlace=dlg.comboBox_4.currentText()
    
    P_Tuneles=dlg.comboBox_5.currentText()
    
    B_W_percentage=float(dlg.lineEdit_7.text()) 
    textoArchivo += "Ancho de banda de reserva=" + str(Bandwidth) + "\n"
    
                         
  
    
    if P_Tuneles=='MPLS':
        textoArchivo += "P_Tuneles=" + str(P_Tuneles) + "\n"
        P_Tuneles=4
        textoArchivo += "P_Tuneles=" + str(P_Tuneles) + "\n"
    elif P_Tuneles=='L2TP':
        textoArchivo += "P_Tuneles=" + str(P_Tuneles) + "\n"
        P_Tuneles=24
        textoArchivo += "P_Tuneles=" + str(P_Tuneles) + "\n"
    elif P_Tuneles=='IPSEC':
        textoArchivo += "P_Tuneles=" + str(P_Tuneles) + "\n"
        P_Tuneles=float(dlg.spinBox.text())
        textoArchivo += "P_Tuneles=" + str(P_Tuneles) + "\n"
    else:
        P_Tuneles=0
        textoArchivo += "P_Tuneles=" + str(P_Tuneles) + "\n"
        
        
    if P_Enlace=='Ethernet 802.1q':
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
        P_Enlace=20
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
    elif P_Enlace=='Ethernet q-inq':
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
        P_Enlace=22
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
    elif P_Enlace=='PPP':
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
        P_Enlace=6
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
    elif P_Enlace=='PPOE':
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
        P_Enlace=24
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
    elif P_Enlace=='Ethernet': 
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
        P_Enlace=18
        textoArchivo += "P_Enlace=" + str(P_Enlace) + "\n"
        
        
    textoArchivo += "\n---Resultados Parciales ----\n\n"
    #Calculamos la longitud de la cabecera para RTP y cRTP que sera 
    #la misma para todos los Codecs. Para el caso de cRTP consideramos
    #que comprime IP/UDP/RTP a un total de 4B. Las colas asociadas al checksum
    #siguen presentes en cRTP
    L_RTP_Cabeceras=int(P_Enlace) + int(P_Tuneles) + 20 + 8 + 12 + 4
    textoArchivo += "L_RTP_Cabeceras=" + str(L_RTP_Cabeceras) + "\n"
    L_cRTP_Cabeceras=int(P_Enlace) + int(P_Tuneles) + 4 + 4
    textoArchivo += "L_cRTP_Cabeceras=" + str(L_cRTP_Cabeceras) + "\n"
    
    #Calculamos el ancho de banda para los dos posibles casos: RTP y cRTP
    #CASO 1: RTP: Tendremos en cuenta el checksum (4bytes)
    BW_SP=np.zeros((dim,1))
    
    for i in range(dim):
        
        L_RTP=8*(Codecs_parametros[i][4]+L_RTP_Cabeceras)
        PPS=(Codecs_parametros[i][0]*1e3)/(8*Codecs_parametros[i][4])
        Bw_llamada=L_RTP*PPS*(1+B_W_percentage)
        BW_SP_RTP=N_lineas*Bw_llamada
        
        L_cRTP=8*(Codecs_parametros[i][4]+L_cRTP_Cabeceras)
        Bw_llamada=L_cRTP*PPS*(1+B_W_percentage)
        BW_SP_cRTP=N_lineas*Bw_llamada
        
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
        
        

    
    textoArchivo_def += textoArchivo
    

def Paso6():
    
    dlg5.close()
    dlg6.show()
    
    dlg6.comboBox.addItems(Codecs)
    

def Paso7():
    
    dlg6.close()
    dlg7.show()
    
    #dlg7.pushButton.hide()
    Ruta_archivo=str(dlg7.lineEdit_paso7.text())
    
    if Ruta_archivo != '':
        CrearArchivo(Ruta_archivo)
        GuardarDatos(textoArchivo_def, Ruta_archivo)
    print("La ruta es:",Ruta_archivo)
    
    return Ruta_archivo
    
    

    
           
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
dlg7=uic.loadUi("Paso7.ui")
dlg_aviso=uic.loadUi("Aviso.ui")


#Placeholders, ¿usar en otros campos?
dlg.lineEdit_5.setPlaceholderText("Probabilidad entre 0-1")
dlg.lineEdit_9.setPlaceholderText("0-1")


#Activamos el evento referente a la cabecera IPESEC 
dlg.comboBox_5.activated.connect(V_Paso1) 

dlg.pushButton.clicked.connect(Paso2) # Pops new window when pushed


dlg2.pushButton.clicked.connect(Paso3)


dlg3.pushButton.clicked.connect(Paso4)


dlg4.pushButton.clicked.connect(Paso5)


dlg5.pushButton_3.clicked.connect(Paso0)


dlg5.pushButton_2.clicked.connect(Paso6)


dlg5.pushButton.clicked.connect(Paso7)


dlg7.pushButton.clicked.connect(Paso7)


dlg.show()
app.exec()

