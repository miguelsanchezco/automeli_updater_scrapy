import requests
import pandas as pd
import os
# from mysqlCRUD import DataLogManager
from modules.mysqlCRUD import DataLogManager
print('trmCalculator.py')


def trmCalculator():
  url = "https://proxy.set-icap.com/seticap/api/estadisticas/estadisticasPromedioCierre/"

  payload = "{\"delay\":15}"
  headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://dolar.set-icap.com',
    'Referer': 'https://dolar.set-icap.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  r = response.json()
  return int(r["data"]["avg"].replace(",","").split(".")[0])


def trmUploadBD():
    # leer el csv trm ingresada manualmente y subirla a BD
    object_connection = DataLogManager("ecommerce")

    df = pd.read_csv("/tmp/trm_manual_input.csv")
    table = "trm"
    object_connection.dfToTableDB(table, df)


def trmGetValue():
  #time.sleep(4)
  # obter el valor del trm desde el csv con el dato descargado de la bd
  path = '/tmp/' 
  # path = path.split('/modules') 
  path_old_date = "/tmp/trm_from_db.csv" 

  df = pd.read_csv(path_old_date)
  print("TRM ", float(df["trm"]))
  return float(df["trm"])


def trmDownload():
  # descargar el último trm en bd
  object_connection = DataLogManager("ecommerce")
  df = object_connection.downloadTrm()

  path = '/tmp/' 
  # path = path.split('/modules') 
  path_old_date = "/tmp/trm_from_db.csv" 
  df.to_csv(path_old_date, index=False)
  print("TRM guardado en csv")


def factorDownload():
  # descargar los factores o multiplicadores, margen, utilidad
  object_connection = DataLogManager("ecommerce")
  df = object_connection.downloadFactor()

  path = '/tmp/' 
  # path = path.split('/modules') 
  path_factores = "/tmp/factores_from_db.csv" 
  df.to_csv(path_factores, index=False)
  print("FACTORES guardados en csv")


def factorGetValues():
  path = '/tmp/' 
  # path = path.split('/modules') 
  path_factores = "/tmp/factores_from_db.csv" 

  df = pd.read_csv(path_factores)
  print(df)

  FACTOR_HIGH = float(df.loc[0,"FACTOR_HIGH"])
  FACTOR_MEDIUM = float(df.loc[0,"FACTOR_MEDIUM"])
  FACTOR_LOW = float(df.loc[0,"FACTOR_LOW"])
  FACTOR_WOO = float(df.loc[0,"FACTOR_WOO"])

  return FACTOR_HIGH, FACTOR_MEDIUM, FACTOR_LOW, FACTOR_WOO



# if __name__ == "__main__":
#   trmUploadBD()
  # trmDownload()
  # print(trmGetValue())