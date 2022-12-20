import json
from os import remove
from datetime import datetime
from random import randint
#import subprocess
#from scrapy.crawler import CrawlerProcess
#from scrapy.utils.log import configure_logging
#from price_updater import UpdaterSpider
from automeli_dataScraper import ScrapeDataProduct, run_spider
from modules.mysqlCRUD import DataLogManager


def handler(event, context):  #event, context
    
    print(f'Event: {event}')
    seller_id = event['seller_id']
    sku = event['sku']
    try:
        title = event['title']
    except:
        title = 'vacio'
    user_category_id = event['user_category']
    listing_type_id = event['listing_type_id']
    access_token = event['access_token']
    test_mode = event['test_mode']  # 1 on, 0 off
    # # # seller_id = '116499542'
    # # # sku = 'holamundo cruel jeje ' 
    # # # user_category_id = 'rassdf'
    # # # listing_type_id = 'gold_special' #gold_pro
    # # # access_token = 'APP_USR-7220664084350595-101516-10023b28e3adebdbd4fe5324fee51822-116499542'
    # # # test_mode = 1

    skus = sku.split(',')   #lista de skus
    titles = title.split(',') #lISTA DE titulos
    skusNew = []
    for sku in skus:
        sku =sku.strip()     #borro espacios en blanco
        skusNew.append(sku)

    # # # skus = skusNew    
    # # # skus = list(set(skus))   #lista de skus sin duplicados
    uniqueTitles = []
    uniqueSkus = []

    for index,sku in enumerate(skusNew):
        if sku not in uniqueSkus:
            uniqueSkus.append(sku)
            if(len(titles)>1):
                uniqueTitles.append(titles[index]) 
            elif(len(titles)==1):
                if titles[0] != 'vacio':
                    uniqueTitles.append(titles[index]) 
                else:
                    uniqueTitles.append('vacio') 
            
    print('uniqueSkus: ',uniqueSkus)
    print('uniqueTitles: ',uniqueTitles)
    skus = uniqueSkus 
    titles = uniqueTitles
  
    path = '/tmp/'
    #path = '/tmp/'#"/data/csv/"
    nameFile = path + f'{seller_id}_response.json'
    try:
        remove(nameFile)
    except:
        pass
    #crear lista de diccionarios para la response
    date = str(datetime.now()).split(".")[0]
    LISTDATA = []
    
    #Verificar plan!
    try:
        ''' Creo un Objeto para conexión con BaseDeDatos'''
        databaseName ='ecommerce_prueba'
        objectDataLog = DataLogManager(databaseName)
        dataUser = objectDataLog.planInfo(seller_id)  #Trae PlanInfo

        status_account  = dataUser.loc[0,'status_account'] 
        usage_type = 'publisher_usage'
        test = ''
        if test_mode == 1:
            test = 'test'
            usage_type = 'testing_usage'

        disponibleCuota = dataUser.loc[0,'publisher_available_quantity'] - dataUser.loc[0,usage_type]
        skusRequested = len(skus)

        if dataUser.loc[0,'status_account'] != 'active':
            defaultValue = f'Tu cuenta no está activa. Tu has sido {dataUser.loc[0,"status_account"]}.'
        elif disponibleCuota >= skusRequested:
            defaultValue = 'No Publicado'
            CuotaSobrepasada = 0
        else:
            CuotaSobrepasada =  skusRequested - disponibleCuota
            defaultValue = f'Alcanzaste el límite de uso! Tu has usado {disponibleCuota} {test} créditos disponibles! - Por favor recarga más créditos :)'
    except Exception as e:
        print(f'error app.py: {e}')
        disponibleCuota = 0
        status_account = 'noexist'
        defaultValue = 'Error: Usuario Inválido!'

    for sku in skus:
        DICTDATA = {}
        DICTDATA['sku'] = sku.strip()
        DICTDATA['id'] = str(randint(0,9999)) + 'null'
        DICTDATA['title'] = 'null'
        DICTDATA['status'] = 'null'
        DICTDATA['permalink'] = 'null'
        DICTDATA['user_price'] = 'null'
        DICTDATA['img'] = 'https://i.ibb.co/5W6X6vX/warning-signs-that-your-travel-expense-management-may-be-out-of-control-300x300.jpg'
        DICTDATA['date_created'] = date
        DICTDATA['message'] = defaultValue
        LISTDATA.append(DICTDATA)

    #guardo archivo json con valores iniciales
    while True:
            try:
                #Guardamos        
                with open(nameFile, 'w') as file:
                #with open(f'{seller_id}.json', 'w') as file:
                    json.dump(LISTDATA, file)
                    
                    print(f'{date} response guardado en archivo json')
                    break
            except Exception as e:
                print(e)
                continue

    #print(subprocess.run('pwd'))
    # print(subprocess.run('ls'))
    # # # # process = CrawlerProcess()
    # # # # process.crawl(ScrapeDataProduct, skus=skus, seller_id = seller_id, user_category_id = user_category_id, listing_type_id=listing_type_id)
    # # # # process.start()
    # # configure_logging()
    # if test_mode == '1':
    #     site_id  = dataUser.loc[0,'site_id'] 
    #     #buscamos para el pais de la persona un usuario test
    #     ''' Creo un Objeto para conexión con BaseDeDatos'''
    #     databaseName ='ecommerce_prueba'
    #     objectDataLog = DataLogManager(databaseName)
    #     dataUserTest = objectDataLog.testUsers(site_id)  #Test User


    if status_account == 'active' and CuotaSobrepasada == 0:
        #access_token = dataUser.loc[0,'access_token'] 
        try:
            run_spider(ScrapeDataProduct, skus, seller_id, user_category_id, listing_type_id, access_token,test_mode,titles)
        except Exception as e:
            print(f'run_spider exception')
   
    while True:
        try:
            # returns JSON object as 
            # a dictionary
            with open(nameFile, 'r',encoding='utf8') as file:       
                DATA = json.load(file)
            print(f'{date} response leido de archivo json app.py')
            break
        except Exception as e:
            print(e)
            continue

    print(DATA)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'http://localhost:3000, http://localhost:9000, https://app.automeli.com', 
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': DATA #json.dumps('Hello from Lambda!')
    }


# # # if __name__ == '__main__':

# # #     jsonResult = handler()
# # #     print('jsonResult: ',jsonResult)