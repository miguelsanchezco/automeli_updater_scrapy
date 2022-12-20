# nymeliapp v 2021.06.09
# Cronometro -------
# Modulo propio de python que se encarga de 
# pasar al script que lo requiera el valor
# del acces_token de mercadolibre.
# Su objetivo es ahorrar recursos, realizando
# una sola llamada a la api de google sheets cada
# vez que se expire los tokens, estos tokens son
# almacenandos en un archivo local txt
# Proxima Actualizad: Usar un archivo CSV para 
# almacenar la data de los tokens y no generar
# tantos archivos.

lapse_time = 18000 # segundos

import time
import os
# tokenUpdater: Modulo que actualiza tokens de mercadolibre
from modules.tokenUpdater import tokenUpdater  


path = '/tmp/' #  #19/07/2021


def access_token_memory(seller_id,databaseName):

    path_old_access_token = path + f"old_access_token{seller_id}.txt"
    path_old_date = path + f"old_date{seller_id}.txt"
    # Verificamos si existe tiempo anterior
    try:

        with open(path_old_date, 'r') as file:
            
            linea = file.readline()
            #print(f'Si existe tiempo anterior, valor: {linea}')
            
    except FileNotFoundError as e:

        #print('No Existe tiempo anterior, lo definimos!')
        old_date = time.time()
        old_date = str(old_date)
        # Escribimos en el archivo old_date
        file = open(path_old_date, "w")
        file. write(old_date + os.linesep)
        #print('Se creo exitosamente el archivo old_date.txt')
 
    # Leemos el tiempo anterior
    file = open(path_old_date, 'r')
    tiempo_anterior = float(file.readline())
    # Tiempo actual
    tiempo_actual = time.time()
    # Calculamos la difencia en segundos
    dif = tiempo_actual - tiempo_anterior
    #print(f'dif: {dif}')

    # Decision - Actualizar o no el access token
    if dif > lapse_time: # segundos
        # Si han transcurrido mas de 5 horas, se debe actualizar
        # LLamo al modulo tokenUpdater y actualizo tokens
        # Llamo al modulo google_sheets - funcion: faccess_log
        # me comunico con la sheet que contiene los access token
        access_token= tokenUpdater(seller_id,databaseName) 

        # if seller_id == 0: #Miguel
        file = open(path_old_access_token, "w")
        file. write(access_token + os.linesep)
        #print('Actualizamos el archivo old_access_token0.txt')


        # Actualizamos el archivo old_date
        old_date = str(time.time())
        #old_date = str(old_date)
        file = open(path_old_date, "w")
        file. write(old_date + os.linesep)


    else: 
        # menor a lapse_time 
        
        # Verificamos si existe token anterior
        try:
            
            with open(path_old_access_token, 'r') as file:
            
                linea = file.readline()
                #print(f'Si existe access_token anterior, valor: {linea}')

                  
        except FileNotFoundError as e:
           
            access_token= tokenUpdater(seller_id,databaseName) 
        
            file = open(path_old_access_token, "w")
            file. write(access_token + os.linesep)

    file = open(path_old_access_token, 'r')
    access_token = str(file.readline())



    access_token = access_token.rstrip('\n') #Eliminamos \n
    #print(f"Enviamos access token al script que lo requiere: {access_token}")
    
    return access_token