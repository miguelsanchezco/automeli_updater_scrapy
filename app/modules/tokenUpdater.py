# nymeliapp v 2021.06.09
# Archivo ejecutandose perpetuamente en la nube
# refresh_token.py 
# Objetivo: Obtener el refresh token de google sheet
# y actualizar el access token cada 5 horas de forma
# infinita, ejecutandose en segundo plano en la nube.
# Archivos requeridos para su funcionamiento: client_secret.json
# Last-updated: 1/06/2021
# Programador: Miguel Sanchez

# Importamos Librerias
#import os
#import meli
#from meli.rest import ApiException

# Librerias Agregadas By Miguel
import json
from datetime import datetime
from modules.mysqlCRUD import DataLogManager
from modules.mercadolibre_app_id import app_meli
from modules.apiMeliController import apiMeliController


def tokenUpdater(seller_id,databaseName):
   
    #with meli.ApiClient() as api_client:
    # Create an instance of the API class
    #api_instance = meli.OAuth20Api(api_client)

    #Solicitamos al modulo mercadolibre_app_id las credenciales de la app
    client_id, client_secret, redirect_uri = app_meli()
    # mercadolibre_app_id
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    obj_connect = DataLogManager(databaseName)
    refresh_token = obj_connect.getRefreshTokenMeli(seller_id)
    print("Refresh desde base de datos: ", refresh_token)
    

    secure = 0
    while secure == 0:

        try:

            # Peticion para obtener token usando un refresh token!!!!!!!!!
            #api_response = api_instance.get_token(grant_type='refresh_token', client_id=client_id,
            #                                    client_secret=client_secret, refresh_token=refresh_token)
            endpoint = 'oauth/token/'
            body = {
                'grant_type': 'refresh_token', 
                'client_id': client_id,
                'client_secret':client_secret,
                'refresh_token':refresh_token
            }
            response = apiMeliController('POST',endpoint,'',body)
            api_response = json.loads(response.text)
            # Save refresh and access token at Google Sheet
            access_token = api_response['access_token']
            refresh_token = api_response['refresh_token']

            #Fecha ultima actualizacion
            date = str(datetime.now()).split(".")[0]
            
            
            obj_connect = DataLogManager(databaseName)
            data_to_update = {"refresh_token": refresh_token, "access_token": access_token, "date_account_updated": date}
            obj_connect.updateAccessTokenMeli(seller_id, **data_to_update)
            print("Access Token and Refresh Token Sent Successfully\n")

            secure = 1 #Salir del WHile

        except Exception as e:
            error = e.status   
            print(f"Error obteniendo access token de Mercadolibre: {error}")
            
            if error == 500 or error == 429: #Error del servidor o Too Many Request
                secure = 0 # Reintentar peticion
                print('reintentado peticion a mercadolibre...')
            else:
                print(e)
                secure = 1 # No reintentar peticion, error desconocido
                
    return access_token        