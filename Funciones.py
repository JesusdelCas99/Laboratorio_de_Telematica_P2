# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 00:48:39 2020

@author: SoftLabs
"""

import numpy as np


###########################################################################
#Calculo del factorial de un numero
def factorial(n): 
    resultado = 1
    i = 1
    while i <= n:
        resultado = resultado * i
        i = i + 1
    return resultado

###########################################################################
#Funcion para el calculo de la probabilidad de bloqueo
def Erlang_B(A,m):
    
    m_fac=factorial(m)
    A=int(np.round(A))
    
    #Calculo del denominador de la funcion Erlang
    num=pow(A,m)/m_fac 

    den=0 #Inicializamos el denominador a 0
    
    for i in range(m+1):
        
        i_fact=factorial(i)
        
        #Calculo del numerador de la funcion Erlang
        den=pow(A,i)/i_fact+den
    
    B=num/den
    
    return B
###########################################################################
#Funcion para el calculo del número de líneas
def Erlang_B2(A,pb):
    #Inicializo variables para controlar bucle y primera iteracion
    diferencia=1e2
    Canales=np.random.randint(100)+1
    iteracion=0
    
    while ((np.abs(diferencia)>1e-3) | iteracion<150) :
        #Calculo la Pb y comparo con la real
        resultado = Erlang_B(A,int(Canales))
        diferencia=pb-resultado
        
        #Dpendiendo de si es mayor o menor; aumento o disminuyo el nº canales
        if diferencia<0:
            Canales+=np.abs(diferencia)*100
        else:
            Canales-=np.abs(diferencia)*100
            if Canales<1:
                Canales=1
                
        Canales=np.ceil(Canales)   
        iteracion+=1   
           
        
    return Canales
           
###########################################################################
#Función para comprobrar si un string contiene un número, teniendo en cuenta
#que este puede ser decimal
    
def isFloat(string):
    try:
        float(string)
        return True
    except:
        return False
    
##########################################################################
#Función para comprobrar si un string contiene una probabilidad, en formato
#de 0 a 1
      
def isProb(string):
    try:
        if (float(string) <= 1) & (float(string) >= 0):        
            return True
        else:
            return False
    except:
        return False         