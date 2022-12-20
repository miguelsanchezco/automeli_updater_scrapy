
import pandas as pd
import os
from random import randint
from modules.mysqlCRUD import DataLogManager

def randomScraperApiKey():
    # Encontrar el archivo con los api keys
    #path = os.getcwd() + '/tmp/'
    path = '/tmp/'
    # path = path.split('/modules') 
    path_old_date = path + "apiKeysScraperapi.csv"
    # ALmacenar los api keys en un dataframe
    df = pd.read_csv(path_old_date)
    NUMERO_API_KEYS = len(df.index)
    # print('NUMERO API KEYS ' ,NUMERO_API_KEYS)
    # if NUMERO_API_KEYS == 0:
    #     print('Error. No hay apikeys para hoy. ')
    # Escoger un apikey de manera aleatoria y retornarlo
    randomNumber = randint(0,NUMERO_API_KEYS-1)  
     
    print(df['apiKey'][randomNumber])
    return df['apiKey'][randomNumber]




def randomScraperApiKeyUploadBD():
    # leer el csv dailyApiKeys y subirlos a BD
    object_connection = DataLogManager("ecommerce")

    df = pd.read_csv("/tmp/dailyApiKeys.csv")
    table = "scraperapi"
    object_connection.dfToTableDB(table, df)


def randomScraperApiKeyDownloadBD(): #randomScraperApiKeyDownloadBD(DateToday):
    # descarga los apikeys de la fecha de hoy
    object_connection = DataLogManager("ecommerce")
    df = object_connection.downloadApiKeysForToday()    # (DateToday)      

    df_keys = df["apikey"]    
    df_keys.rename("apiKey",inplace = True) #renaming a serie (not dataframe) 
    print('apikeys: \n',df_keys)
    # path = '/tmp/' 
    # path = path.split('/modules') 
    path_apikeys = "/tmp/apiKeysScraperapi.csv" 

    df_keys.to_csv(path_apikeys, index=False)
    print("Apikeys guardadas en csv")

if __name__ == '__main__':
    #randomScraperApiKeyUploadBD()    
    randomScraperApiKeyDownloadBD()
    