
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient
client = MongoClient("mongodb+srv://mauricio123:1979Mono@cluster0.msw9f.mongodb.net/?retryWrites=true&w=majority&tls=true")
#db = client.get_database('automeli')
db = client['automeli']
#datePrices = db.datePrices
datePrices = db['datePrices']
'''
    Scrapy
    Scrapeamos los precios de los productos en products_info : Base de Datos AWS
    Last Updated: 12/08/2022

'''
# from scrapy.crawler import CrawlerProcess
from urllib.parse import urlencode
from datetime import datetime, timedelta
import scrapy

from math import floor
# ''' Imports para manejo de errores 404 '''
#from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
from modules.cookiesRefresh import cookiesRefresh

from modules.randomScraperApiKey import randomScraperApiKeyDownloadBD #ScraperAPI apiKey
from modules.mysqlCRUD import DataLogManager
from modules.trmCalculator import trmDownload
# from cookiesRandom import cookiesRandom
# from sku_encrypt import decrypt, encrypt
'''Descargamos los APIKEY de ScraperAPI para las cookies'''
randomScraperApiKeyDownloadBD()
"""Actualizar el csv de TRM primero"""
trmDownload()

from modules.selectores_css import selectores_css # Si esta linea se pone antes de trmDownload() produce un bug 
                                                  # la TRM se lee del archivo csv sin actualizar y esto 
                                                  # no es el funcionamiento esperado.

HEADERS = {
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-type': 'application/x-www-form-urlencoded',
  'Connection': 'keep-alive',
  'Referer': 'https://www.amazon.com/',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1'
}
 
''' Clase Spider '''
class UpdaterSpider(scrapy.Spider):

    # Nombre Spider
    name = "updater_spider"

    databaseName = 'ecommerce_prueba'
    urls=[]
    INICIO_CORREGIDO = 0
    df = []
    amazon_site  = ''
    meli_site_id = ''
    zip_code = '00000'
    seller_id = ''  
    mtactive = 0
    mtauto = 0
    mtdays = 0
    
    # Configuraciones Spider and exit file
    custom_settings = {

        'CONCURRENT_REQUESTS' : 15, #ScraperAPI Configuration
        'RETRY_TIMES': 3, # ScraperAPI Recommendation = 5
        'ROBOTSTXT_OBEY' : False,
        'CONCURRENT_REQUESTS_PER_IP' : 15  
    }


    def __init__(self, seller_id=None,*args, **kwargs):
        super(UpdaterSpider, self).__init__(*args, **kwargs)

        print("seller_id {}".format(seller_id))
        self.seller_id = seller_id

        #print(df.head(5))
        ''' Creo un Objeto para conexión con BaseDeDatos'''
        objectDataLog = DataLogManager(self.databaseName)

        # df = objectDataLog.extractAllData()
        self.df = objectDataLog.extractDataProductsInfo(self.seller_id)  #Trae todo products_info
        print(f'df.shape: {self.df.shape}')
                
        
        for sku in self.df["sku"]:     
            self.urls.append('https://www.amazon.com/-/es/dp/'+ sku)

        ''' Creo un Objeto para conexión con BaseDeDatos'''
        objectDataLog = DataLogManager(self.databaseName)
        self.dataUser = objectDataLog.extractUserData(self.seller_id)  #Trae parameters
        print(f'dataUser: {self.dataUser}')

        self.amazon_site  = self.dataUser.loc[0,'amazon_site']
        self.meli_site_id = self.dataUser.loc[0,'meli_site_id']
        self.zip_code = self.dataUser.loc[0,'zip_code']
        self.mtactive  = self.dataUser.loc[0,'manufacturing_time_active']
        self.mtauto = self.dataUser.loc[0,'manufacturing_time_auto']
        self.mtdays = self.dataUser.loc[0,'manufacturing_time_days']

        if self.meli_site_id == 'MLM': 
            self.countryName = 'México Mexico'
        elif self.meli_site_id == 'MCO':
            self.countryName = 'Colombia'
        elif self.meli_site_id == 'MLA':
            self.countryName = 'Argentina'
        elif self.meli_site_id == 'MLC':
            self.countryName = 'Chile'
        elif self.meli_site_id == 'MEC':
            self.countryName = 'Ecuador'
        else:
            self.countryName = 'address dirección'
        

    def proxyFuncion(self, url):
        
        #COUNTRY_CODE = 'us' #Estados Unidos
        #API_KEY = randomScraperApiKey() #Modulo propio, genera apikey aleatorio
        API_KEY ='fa92d233f85e48889c92df47248b944dc7242844c54'

        payload = {'token': API_KEY, 
                   'url': url,
                   'customHeaders':'true'}
                   #'geoCode': COUNTRY_CODE}

        proxy_url = 'http://api.scrape.do/?' + urlencode(payload)
        return proxy_url

    # Funcion Start Request
    def start_requests(self):
      
        for index, url in enumerate(self.urls):
   
            COOKIES = cookiesRefresh(index,self.seller_id,self.amazon_site,self.meli_site_id,self.zip_code)
        
            yield scrapy.Request(url=self.proxyFuncion(url), 
                                callback=self.parse,  # self.proxyFuncion(url)
                                errback=self.errback, # Manejo de errores 404 
                                dont_filter=True,
                                headers=HEADERS,
                                cookies=COOKIES,
                                cb_kwargs={'url' : url , "index": index + self.INICIO_CORREGIDO})     #, meta=meta)

    # Funcion para manejo de errores 404 Fuente: 
    # https://docs.scrapy.org/en/latest/topics/request-response.html#
   
    def errback(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):

            response = failure.value.response
            url = response.url
            sku = (response.url).split('%2F').pop().split('&')[0]
            print('sku errback: ',sku)
            
            buscar_index = list(self.df[self.df["sku"] == sku].index)
            index = buscar_index[0] if len(buscar_index) > 0 else None
            print('index errback: ',index)
            #index = failure.request.cb_kwargs["index"]
            #url = failure.request.cb_kwargs['url']
            #sku = df.loc[index, "sku"]
            
            self.logger.error('HttpError on %s', response.url)
            print(f'status_code: {response.status}')
            print('url errback: ',url)
            url = 'https://www.amazon.com/-/es/dp/'+ sku
            print('url errback limpia para reintento: ',url)
            
            
            if response.status == 403 or response.status == 429 or response.status == 400:  # ApiKey Limite 1000 rquests/mes o demasiadas solicitudes con la misma api key
                print(f'ERROR {response.status} - Reintentar Request\n')
   
                COOKIES = cookiesRefresh(index,self.seller_id,self.amazon_site,self.meli_site_id,self.zip_code)
                #Reintentar requests 
                yield scrapy.Request(url=self.proxyFuncion(url), #self.proxyFuncion(url)
                                    callback=self.parse,
                                    errback=self.errback, #Manejo de errores 
                                    dont_filter=True,
                                    headers=HEADERS,
                                    cookies=COOKIES,
                                    cb_kwargs={'url' : url, "index": index })#+ INICIO_CORREGIDO})#, meta=meta)


            elif response.status == 404:
                # la pag de amazon ya no existe    
                print('Item Eliminado de Amazon')
                print(f'sku eliminado: {sku}')
                #Fecha actual 
                date =  str(datetime.now()).split(".")[0]              
                #id_sku = self.df.loc[index, "id_sku"]  #+ INICIO_CORREGIDO
                objectDataLog = DataLogManager(self.databaseName) # <<<--- agregado
                objectDataLog.updateProducts("products_info_customers", sku,"sku", **{"amz_status": "Eliminado", "stock_quantity": 0, "date_updated_amazon":date})
                
                        
    # Funcion Parse 
    def parse(self, response, **kwargs):
        
        index = kwargs["index"]
        #print('index PARSE: ',index)
        sku = self.df.loc[index, "sku"]
        #id_sku = self.df.loc[index, "id_sku"]
        print(f"**************  SKU: {sku}   ****************")
        #Fecha actual 2021-06-07 22:50:30
        date =  str(datetime.now()).split(".")[0]
        #date = str(datetime.now() + timedelta(days=2)).split(".")[0]
        print(f'\nDATE: {date}')
        
        #Obtenemos el peso max del producto de la base de datos.        
        maxWeigth = int(self.df.loc[index, "max_weigth"])
        

        # MODULO QUE CALCULA PRECIO, AVAILABLE_Q AND MANUF_TIME
        [scraped_price,available_quantity,MANUFACTURING_TIME,weigth,volume,pesoVol,maxWeigth,
        USD_total,country,vendedor,despachador,shippingCost,taxes] = selectores_css(response,maxWeigth,self.mtactive,self.mtauto,self.mtdays)

        #USD_total = USD_total *1.2
        
        to_update = {}

        if USD_total == 0: #Cargamos Datos Anteriores
            to_update["regular_price"] = self.df.loc[index, "regular_price"]
            to_update["sale_price"] = self.df.loc[index, "sale_price"]
        else: 
            if USD_total < self.df.loc[index, "regular_price"] and self.df.loc[index, "regular_price"]>0: # new < old
                to_update["sale_price"] = USD_total
                to_update["regular_price"] = self.df.loc[index, "regular_price"]
     
            else:
                to_update["sale_price"] = USD_total
                to_update["regular_price"] = USD_total

        
        to_update["amz_site"] = self.amazon_site 
        to_update["meli_site_id"] = self.meli_site_id 
        to_update["total_price"] = USD_total
        to_update["scraped_price"] = scraped_price
        to_update["shipping_cost"]  =   shippingCost 
        to_update["taxes"]  =   taxes 
        to_update["stock_quantity"]  =   available_quantity 
        to_update["manufacturing_time"] = MANUFACTURING_TIME
        to_update["max_weigth"] = maxWeigth
        if available_quantity > 0:
            to_update["amz_status"] = 'Disponible'
        else:
            to_update["amz_status"] = 'Agotado'
        to_update["date_updated"] = date
        
        #Actualizar MongoDB
        # db = client.get_database('automeli')
        # datePrices = db.datePrices
        TRM =4500
        id_meli = self.df.loc[index, "id_meli"]
        regPrice =  to_update["regular_price"]*TRM
        salePrice = to_update["sale_price"]*TRM
        newHistoryPrice = {'date': date, 'regPrice': regPrice, 'salePrice': salePrice, 'amazonPrice': USD_total}
        newProductObject = {
            'id_meli':id_meli,
            'seller_id':seller_id,
            'sku':sku,
            'site_id':self.meli_site_id,
            'amazon_site':self.amazon_site,
            "history_prices":[newHistoryPrice]
        }

        myquery = {'id_meli':id_meli}
        #datePrices.insert_one(productInfo)
        result = datePrices.find_one(myquery)
        if result == None:
            datePrices.insert_one(newProductObject)
        else:
            newvalues = { "$push": { "history_prices": newHistoryPrice}} 
            datePrices.update_one(myquery, newvalues)
        
        if  self.countryName in country or self.zip_code in country:
            #Diccionario donde se almacenara la data a exportar
            print(f'country or city:{country}')
            # comparacion precio anterior y actual
            print(f'New_total_price: {USD_total}')
            #if (self.df.loc[index, "sale_price"]) != 0:
            total_price_anterior = (self.df.loc[index, "total_price"])
            #else:
            #scraped_price_anterior = (self.df.loc[index, "regular_price"])
            print(f'Old_total_price: {total_price_anterior}')
            print(f'New_available_quantity: {available_quantity}')
                        
            available_quantity_anterior = int(self.df.loc[index, "stock_quantity"])
            print(f'Old_available_quantity: {available_quantity_anterior}')
            #print(f'\n\n\nPRECIOOOO BASEEE DE DATOOOSSS {sku}: {scraped_price_anterior}')
            #print(f'PRECIOOOO NUEVO {sku}: {scraped_price}\n\n\n')
            
            
            if (USD_total == total_price_anterior and 
                available_quantity == available_quantity_anterior): 
                # Dado que ambas se cumplen!
                print('\n @ Precio y disponibilidad siguen igual @')
                # No se actualiza mercadolibre, tampoco base de datos.
                # to_update = {}         #PROVISIONALLLL
                # to_update["date_updated_amazon"] = date      #PROVISIONALLLL                  
                to_update["changed"] = '--'       
                print("DATA DICT TO UPDATE: ", to_update)
                objectDataLog = DataLogManager(self.databaseName)
                objectDataLog.updateProducts("products_info_customers",sku,"sku", **to_update)
               
            else:
                 # Si el precio y dispo. cambiaron, debo actualizar database
                print('\n @ Precio y disponibilidad Cambiaron @')
                if USD_total > total_price_anterior:
                    to_update["changed"] = 'Subió'
                elif USD_total < total_price_anterior:
                    to_update["changed"] = 'Bajó'
                else:
                    to_update["changed"] = 'Estable'

            
                print("DATA DICT TO UPDATE: ", to_update)
                objectDataLog = DataLogManager(self.databaseName)
                objectDataLog.updateProducts("products_info_customers",sku,"sku", **to_update)

               
        else:
            print('captcha - repetir request!')
            url = 'https://www.amazon.com/-/es/dp/' + str(sku)
            
            COOKIES = cookiesRefresh(index,self.seller_id,self.amazon_site,self.meli_site_id,self.zip_code)
            yield scrapy.Request(url=self.proxyFuncion(url), 
                                 callback=self.parse,  # self.proxyFuncion(url)
                                 errback=self.errback, #Manejo de errores 404 
                                 dont_filter=True,     #, meta=meta)    
                                 headers=HEADERS,
                                 cookies=COOKIES,
                                 cb_kwargs={'url' : url , "index": index })


if __name__ == "__main__":

    print('hola Mundo Inicio')
    seller_id = '116499542'
    process = CrawlerProcess()
    process.crawl(UpdaterSpider, seller_id = seller_id)
    process.start()
    print('hola Mundo Fin')