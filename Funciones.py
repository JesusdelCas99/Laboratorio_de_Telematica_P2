# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 00:48:39 2020

@author: SoftLabs
"""

#Ponedme la autoría de los ficheros, con nombres y apellidos.
#¿Quién es SoftLabs?

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
