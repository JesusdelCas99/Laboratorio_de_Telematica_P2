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
  
########################################################################### 
    
def Paso2(): 
    
    dlg2.show()   
    
    global Codecs_parametros
    global Codecs
    
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

    #Seleccionamos de la base de datos los codecs que tengan MOS mayor igual
    #al planteado por el usuario
    conn = sql.connect('DataBaseMOS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Codecs_DataBase where MOS >=' + str(MOS))
    records = cursor.fetchall()
    
    
    
    Codecs_parametros=np.zeros((len(records),9))
    Codecs=list()
    
    #Agrupo todos los codecs en una lista y sus parámetros en una matriz
    z=0
    
    for raw in records:        
          Codecs.append(raw[0])
          for j in range(1,10):             
              Codecs_parametros[z,j-1]=float(raw[j])
          z+=1
            
    dlg2.lineEdit.setText(dlg.comboBox_2.currentText())
    dlg2.lineEdit.setReadOnly(True)   
##########################################################################

def Paso3():
    
    #Mostramos la ventana referente al paso 3
    dlg3.show() 
    
    global Retardo_total
    global R_final
    global dim #Numero de Codecs seleccionados
    
    Jitter=float(dlg.lineEdit_11.text())*10^(-3)
    Retardo_red=float(dlg.lineEdit_10.text())*10^(-3)
    Retardo_VoIp=dlg.comboBox.text()
    Retardo_G114=dlg.comboBox_3.text()
    
                       
    if Retardo_VoIp=='aceptable':
        Retardo_VoIp=150*10^(-3)
    elif Retardo_VoIp=='moderado':
        Retardo_VoIp=400*10^(-3)
    else:
        Retardo_VoIp=1
        
    
    if Retardo_G114=='Muy satisfecho':
        Retardo_G114=200*10^(-3)
    elif Retardo_G114=='satisfecho':
        Retardo_G114=287.5*10^(-3)
    elif Retardo_G114=='Alguno insatisfecho':
        Retardo_G114=387.5*10^(-3)
    elif Retardo_G114=='Mucho insatisfecho':
        Retardo_G114=550*10^(-3)
    elif Retardo_G114=='Casi todos insatisfechos':
        Retardo_G114=1
    
    Retardo_total=min(Retardo_G114,Retardo_VoIp)
    
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
        n_look_ahead=3*10^(-3)
        
        #Retraso de paquetizacion
        VPS=Codecs_parametros[i][4]/((Codecs_parametros[i][0])*10^(3))
        R_final[i]=VPS
        
        #Retraso algoritmico
        R_final[i]=R_final[i]+n_look_ahead
        
        #Tiempo de ejecucion de la compresion. Consideramos un 10% de CSI
        #por trama
        R_final[i]=R_final[i]+0.1*Codecs_parametros[i][2]
        
        #Añadimos el retardo de red
        R_final[i]=R_final[i]+Retardo_red
        
        #Retardo de decodificacion
        R_final[i]=R_final[i]+0.1*Codecs_parametros[i][2]
        
        #Retardo de buffer antijitter
        R_fin1=int((1.5*Jitter)/VPS)*VPS+R_final[i]
        R_fin2=int((2*Jitter)/VPS)*VPS+R_final[i]
        
        #En caso de obtener para los dos tamaños de buffer antijitter un 
        #retardo que entre dentro de las cotas, escogemos el que tenga mayor
        #tamaño de buffer antijitter
        if R_fin2<Retardo_total:
            R_final[i]=R_fin2
            
            #Numero de paquetes a almacenar por el buffer antijitter
            Storage_P[i]=int((2*Jitter)/VPS)
        else:
            R_final[i]=R_fin1
            
            #Numero de paquetes a almacenar por el buffer antijitter
            Storage_P[i]=int((1.5*Jitter)/VPS)
                                    
           
# Calculo de GoS número de líneas en una ventana adicional #################
def Paso4():
    
    #Mostramos la ventana referente al paso 4
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
    
    #Calculamos el numero de lineas en base a la funcion Erlang_B2
    N_lineas=Erlang_B2(BHT,float(dlg.lineEdit_9.text()))
    dlg4.lineEdit_3.setText(str(N_lineas))
    dlg4.lineEdit_3.setReadOnly(True) 
    

def Paso5():
    
    #Mostramos la ventana referente al paso 5
    dlg5.show()
    
    #Colocamos el ancho de banda con variable global
    global Bandwidth

    #Calculamos el ancho de banda global
    Bandwidth=4*10^(6)  #Esto es algo que se deberia de dar no? 
    
    #Extraemos de la GUI los parametros de cabeceras del paquete
    P_Enlace=dlg.comboBox_5.text()
    P_Tuneles=dlg.comboBox_4.text()
    B_W_percentage=float(dlg.lineEdit_7.text()) 
    
    if P_Tuneles=='MPLS':
        P_Tuneles=4
    elif P_Tuneles=='L2TP':
        P_Tuneles=24
    elif P_Tuneles=='IPSEC':
        P_Tuneles=float(dlg.SpinBox.text())
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
    L_RTP_Cabeceras=P_Enlace+P_Tuneles+20+8+12+4
    L_cRTP_Cabeceras=P_Enlace+P_Tuneles+4+4
    
    #Calculamos el ancho de banda para los dos posibles casos: RTP y cRTP
    #CASO 1: RTP: Tendremos en cuenta el checksum (4bytes)
    BW_SP=np.zeros((dim,1))
    
    for i in range(dim):
        
        L_RTP=8*(Codecs_parametros[i][4]+L_RTP_Cabeceras)
        PPS=(Codecs_parametros[i][0]*10^(3))/(8*Codecs_parametros[i][4])
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
            
        #FALTA SACAR POR PANTALLA TODOS LOS DATOS Y VER COMO DISEÑAMOS
        #CADA UNA DE LAS VENTANAS PARA SACAR LOS DATOS
            
        
           
###########################################################################
################## PROGRAMACION BACK-END ##################################
###########################################################################

                            
app=QtWidgets.QApplication([])

#Cargamos el archivo '.ui' diseñado mediante Qt Designer
dlg=uic.loadUi("VoIp_SoftLab.ui")


#dlg.spinBox.setVisible(False)
    
dlg2=uic.loadUi("Paso2.ui")
dlg4=uic.loadUi("Paso4.ui")
#Falta crear la nueva ventana para el paso 3 y 5


#Placeholders, ¿usar en otros campos?
dlg.lineEdit_5.setPlaceholderText("Probabilidad entre 0-1")
dlg.lineEdit_9.setPlaceholderText("0-1")


dlg.pushButton.clicked.connect(Paso2) # Pops new window when pushed



dlg2.pushButton.clicked.connect(Paso3)



dlg.show()
app.exec()
