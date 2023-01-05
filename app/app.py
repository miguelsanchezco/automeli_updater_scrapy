
from updater_automeli import UpdaterSpider, run_spider
from modules.mysqlCRUD import DataLogManager
from datetime import datetime
#from random import randint
import json
import time

def handler(event, context):  #event, context
    
    start = time.time()

    print('event: ',event)

    try:
        body =  json.loads(event['Records'][0]['body'])
        print(f'event: {body}, type: {type(body)}')
        print('primary_key:',body['primary_key'])
        print('seller_id:',body['seller_id'])
        print('pack1000:',body['pack1000'])
        print('quantity_pack1000:',body['quantity_pack1000'])
        primary_key = body['primary_key'] #Para Base de Datos
        seller_id = body['seller_id']
        pack1000 = body['pack1000']
        quantity_pack1000 = body['quantity_pack1000']
    except Exception as e:
        print(f'error: {e}')
        primary_key = 0
        seller_id = 0
        pack1000 = 0
        quantity_pack1000 = 0

    #crear lista de diccionarios para la response
    date = str(datetime.now()).split(".")[0]
    print(f'\nFECHA: {date}')
    dict_to_update = {}
    dict_to_update['status_scrapy'] = 'Started'
    dict_to_update['status'] = 'Procesando...'
    table = 'update_schedule'
    dataBaseName = 'ecommerce_prueba'
    objectMysql = DataLogManager(dataBaseName)
    objectMysql.updateAnyTable(table, primary_key, 'id', **dict_to_update )

    if seller_id != 0 and pack1000 != 0 and quantity_pack1000 != 0:
        try:
            run_spider(UpdaterSpider, seller_id, pack1000, quantity_pack1000)
            
            #Guardar en Base de datos!
            
            dict_to_update['status_scrapy'] = 'Finished'
      
        except Exception as e:
            print(f'run_spider exception')
            
            #Guardar en Base de datos!
           
            dict_to_update['status_scrapy'] = 'Exception'

    tiempo_transcurrido = time.time() - start
    print(f'TIEMPO TRANSCURRIDO: {tiempo_transcurrido}')

    dict_to_update['time_lapse_seconds'] = str(tiempo_transcurrido).split('.')[0] 
    table = 'update_schedule'
    dataBaseName = 'ecommerce_prueba'
    objectMysql = DataLogManager(dataBaseName)
    objectMysql.updateAnyTable(table, primary_key, 'id', **dict_to_update )


    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'http://localhost:3000, http://localhost:9000, https://app.automeli.com', 
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': dict_to_update['status_scrapy'] #json.dumps('Hello from Lambda!')
    }

