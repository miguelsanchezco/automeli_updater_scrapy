'''
    Scrapy
    Scrapeamos los precios de los productos en products_info : Base de Datos AWS
    Last Updated: 17/01/2023

'''
from modules.priceFactorsConversion import priceFactorsConversion

from crochet import setup, wait_for
from scrapy.crawler import CrawlerRunner
from modules.api_imagenes_json import img_depuration
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlencode
from datetime import datetime, timedelta
from modules.mongoCRUD import mongoSaveProduct
import scrapy
import os
import sys

# ''' Imports para manejo de errores 404 '''
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
from modules.cookiesRefresh import cookiesRefresh
#from twisted.internet.error import DNSLookupError

# from modules.randomScraperApiKey import  randomScraperApiKeyDownloadBD #ScraperAPI apiKey
from modules.mysqlCRUD import DataLogManager
# from modules.trmCalculator import trmDownload

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
 
setup()

''' Clase Spider '''
class UpdaterSpider(scrapy.Spider):

    # Nombre Spider
    name = "updater_spider"
    # amazon_site  = 'amazon.com'
    idcookie = ''
    zip_code = ''
    quantity_pack1000 = '' 
    countryName = ''

    ################
    databaseName = 'ecommerce_prueba'
    urls=[]
    df = []
    amazon_site  = ''
    meli_site_id = ''
    geo_result_id = ''
    zip_code = '00000'
    seller_id = ''  
    mtactive = 0
    mtauto = 0
    mtdays = 0
    COOKIES = {}
    ################


    custom_settings = {

        'DOWNLOAD_TIMEOUT': 30, #30 segundos 
        # 'HTTPCACHE_ENABLED':False,
        'CONCURRENT_REQUESTS' : 15, #ScraperAPI Configuration
        'RETRY_TIMES': 3, # ScraperAPI Recommendation = 5
        'ROBOTSTXT_OBEY' : False,
        'CONCURRENT_REQUESTS_PER_IP' : 15  
    }

    def __init__(self, seller_id='', pack1000='', quantity_pack1000='',*args, **kwargs):
        super(UpdaterSpider, self).__init__(*args, **kwargs)
        self.urls=[]
        self.seller_id = seller_id
        self.pack1000 = pack1000 #orden del pack de 1000 productos a actualizar
        self.quantity_pack1000 = quantity_pack1000
        print(f'ESTAMOS EN EL CONSTRUCTOR:  seller_id: {self.seller_id} pack1000: {self.pack1000} quantity_pack1000: {self.quantity_pack1000}')
        #debemos recibir estos parametros

        #Traemos los productos correspondientes a actualizar
        ''' Creo un Objeto para conexión con BaseDeDatos'''
        self.databaseName = 'ecommerce_prueba'
        objectDataLog = DataLogManager(self.databaseName)
        self.df = objectDataLog.productsToUpdate(seller_id)  #Trae todo products_info_customers
        print(f'self.df.shape: {self.df.shape}')

        inicio = 0
        fin = 0

        if pack1000 <= quantity_pack1000:
            inicio = (pack1000-1)*1000
            fin =  (pack1000)*1000

        cantidad_real_productos = self.df.shape[0]  #cantidad real de productos listos a actualizar

        if(cantidad_real_productos<=quantity_pack1000*1000):
            if (pack1000 == quantity_pack1000): #si es el ultimo pack
                fin = cantidad_real_productos
        

        print(f'inicio: {inicio}')
        print(f'fin: {fin}')


        try:
            self.df = self.df.iloc[inicio: fin, :]
            self.df.reset_index(drop=True, inplace=True) #Para que los indices empiecen en 0
            print(self.df.head(10))
        except:
            print('no hay esa cantidad de productos')
        

        ''' Creo un Objeto para conexión con BaseDeDatos'''
        objectDataLog = DataLogManager(self.databaseName)
        self.dataUser = objectDataLog.extractUserData(seller_id)  #Trae parameters
        #print(f'dataUser: {self.dataUser}')
        self.amazon_site  = self.dataUser.loc[0,'amazon_site']
        self.meli_site_id = self.dataUser.loc[0,'meli_site_id']
        self.geo_result_id = self.dataUser.loc[0,'geo_result_id']
        self.zip_code = self.dataUser.loc[0,'zip_code']
        self.mtactive  = self.dataUser.loc[0,'manufacturing_time_active']
        self.free_shipping_promo  = self.dataUser.loc[0,'free_shipping_promo']
        self.mtauto = self.dataUser.loc[0,'manufacturing_time_auto']
        self.mtdays = self.dataUser.loc[0,'manufacturing_time_days']
        self.use_locker =  int(self.dataUser.loc[0,'use_locker'])
        self.meli_currency = self.dataUser.loc[0,'meli_currency']
        if self.geo_result_id == 'MLM': 
            self.countryName = 'México Mexico'
        elif self.geo_result_id == 'MCO':
            self.countryName = 'Colombia'
        elif self.geo_result_id == 'MLA':
            self.countryName = 'Argentina'
        elif self.geo_result_id == 'MLC':
            self.countryName = 'Chile'
        elif self.geo_result_id == 'MEC':
            self.countryName = 'Ecuador'
        else:
            self.countryName = self.zip_code #Estados Unidos

        for sku in self.df["sku"]:
            
            self.urls.append(f'https://www.{self.amazon_site}/-/es/dp/{str(sku)}?th=1&psc=1')
            #url = f'https://www.{self.amazon_site}/-/es/dp/{sku}?th=1&psc=1'


    def proxyFuncion(self, url):
        
        #COUNTRY_CODE = 'us' #Estados Unidos
        #API_KEY = randomScraperApiKey() #Modulo propio, genera apikey aleatorio
        API_KEY ='c2beda536e3f48bb9ededf793f4e6b0bf32639f621a'

        payload = {'token': API_KEY, 
                   'url': url,
                   'customHeaders':'true'}
                   #'geoCode': COUNTRY_CODE}

        proxy_url = 'http://api.scrape.do/?' + urlencode(payload)
        return proxy_url


    # Funcion Start Request
    def start_requests(self):

        self.COOKIES,self.idcookie = cookiesRefresh(0,self.seller_id,self.amazon_site,self.geo_result_id,self.zip_code)
        print(f'len(self.urls): {len(self.urls)}')
        for index, url in enumerate(self.urls):
            
            print(f'URL: {url}')    
            yield scrapy.Request(url=self.proxyFuncion(url), 
                                callback=self.parse,  # self.proxyFuncion(url)
                                errback=self.errback, # Manejo de errores 404 
                                dont_filter=False,
                                headers=HEADERS,
                                cookies=self.COOKIES,
                                cb_kwargs={'url' : url , "index": index, "idcookie":self.idcookie})     #, meta=meta)

    # Funcion para manejo de errores 404 Fuente: 
    # https://docs.scrapy.org/en/latest/topics/request-response.html#
   
    def errback(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):

            response = failure.value.response
            url = response.url
            sku = (response.url).split('dp%2F').pop().split('%2F')[0].split('%3F')[0]  # Metodo API
            print('sku errback: ',sku)

            buscar_index = list(self.df[self.df["sku"] == sku].index)
            index = buscar_index[0] if len(buscar_index) > 0 else None
            print('index errback: ',index)
            #index = failure.request.cb_kwargs["index"]
            #url = failure.request.cb_kwargs['url']
            #sku = self.df.loc[index, "sku"]
            
            
            self.logger.error('HttpError on %s', response.url)
            print(f'status_code: {response.status}')
            print('url errback: ',url)
            url = f'https://www.{self.amazon_site}/-/es/dp/{str(sku)}?th=1&psc=1'
            print('url errback limpia para reintento: ',url)
            
            
            if response.status == 403 or response.status == 429 or response.status == 400:  # ApiKey Limite 1000 rquests/mes o demasiadas solicitudes con la misma api key
                print(f'ERROR {response.status} - Cambiar ApiKey ScraperAPI\n')

                  
                #COOKIES = cookiesRefresh(index,self.seller_id,self.amazon_site,self.meli_site_id,self.zip_code)
                #Reintentar requests - cambiar apiKey scraperapi
            
                yield scrapy.Request(url=self.proxyFuncion(url), #self.proxyFuncion(url)
                                    callback=self.parse,
                                    errback=self.errback, #Manejo de errores 
                                    dont_filter=True,
                                    headers=HEADERS,
                                    cookies=self.COOKIES,
                                    cb_kwargs={'url' : url, "index": index, "idcookie":self.idcookie })


            elif response.status == 404:
                # Si ocurre un error 404 significa que 
                # la pag de amazon ya no existe    
                print('Item Eliminado de Amazon')
                print(f'sku eliminado: {sku}')
                #Fecha actual 
                date =  str(datetime.now()).split(".")[0]              
                id_meli = self.df.loc[index, "id_meli"]  #+ INICIO_CORREGIDO
                objectDataLog = DataLogManager(self.databaseName) # <<<--- agregado
                objectDataLog.updateProducts("products_info_customers", id_meli,"id_meli", **{"amz_status": "Eliminado", "stock_quantity": 0, "date_updated":date})
                
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url) 
            print('TimeoutError Reintentar Request!')       


    # Funcion Parse 
    def parse(self, response, **kwargs):

        sku = (response.request.url).split('dp%2F').pop().split('%2F')[0].split('%3F')[0] # Metodo API
        print(f'skuuu: {sku}')
        #  B0BB1N54QQ%3Fth%3D1%26psc%3D1&customHeaders=true
        buscar_index = list(self.df[self.df["sku"] == sku].index)
        print(f'buscar_index: {buscar_index}')
        index = buscar_index[0] if len(buscar_index) > 0 else None
          
        # index = kwargs["index"]
        #print('INDEX PARSE: ',index)

        #cantidad = self.df.shape[0]
        #print('self.df.shape[0]: ',cantidad)
        # if cantidad == index: #Bug detectado!
        #     index = index -1
        #     print('INDEX PARSE CORREGIDO: ',index)
       
        #sku = self.df.loc[index, "sku"]
        id_meli = self.df.loc[index, "id_meli"]
        print(f"**************  id_meli: {id_meli}  SKU: {sku}   ****************")
        
        date =  str(datetime.now()).split(".")[0]
        print(f'\nDATE: {date}')
        
        #imagenes
        data_to_yield = {}
        data_to_yield,list_images = img_depuration(data_to_yield,response) #data_to_yield, response  !!!!
        #print('LIST IMAGES: ',list_images)
        try:
            NewImagen = list_images[0]
        except:
            NewImagen = self.df.loc[index, "image"]

        

        #Obtenemos el peso max del producto de la base de datos.        
        maxWeigth = int(self.df.loc[index, "max_weigth"])
  

        # MODULO QUE CALCULA PRECIO, AVAILABLE_Q AND MANUF_TIME
      
        [scraped_price,available_quantity,MANUFACTURING_TIME,weight,volume,pesoVol,maxWeigth,
        USD_total,country,vendedor,despachador,shippingCost,taxes] = selectores_css(response,maxWeigth,self.mtactive,self.mtauto,self.mtdays,self.use_locker,self.geo_result_id,self.free_shipping_promo)

        # # price_to_meli = int(round(price_to_meli))
        to_update = {}
        

        if(NewImagen != self.df.loc[index, "image"]):
            to_update['image_changed'] = 1
        else:
            to_update['image_changed'] = 0

        if USD_total == 0: #Cargamos Datos Anteriores
            to_update["regular_price"] = self.df.loc[index, "regular_price"]
            to_update["sale_price"] = self.df.loc[index, "sale_price"]
            to_update["total_price"] = self.df.loc[index, "total_price"]
            to_update["scraped_price"] = self.df.loc[index, "scraped_price"]
            to_update["shipping_cost"]  =  self.df.loc[index, "shipping_cost"]
            to_update["taxes"]  =  self.df.loc[index, "taxes"]

        else: 
            if USD_total < self.df.loc[index, "regular_price"] and self.df.loc[index, "regular_price"]>0: # new < old
                to_update["sale_price"] = USD_total
                to_update["regular_price"] = self.df.loc[index, "regular_price"]
     
            else:
                to_update["sale_price"] = USD_total
                to_update["regular_price"] = USD_total
            
            to_update["total_price"] = USD_total
            to_update["scraped_price"] = scraped_price
            to_update["shipping_cost"]  =  shippingCost
            to_update["taxes"]  =  taxes

        
        meli_price, mshops_price =  priceFactorsConversion(to_update["total_price"],self.seller_id,self.databaseName,self.meli_site_id)
        
        meli_sale_price_anterior = self.df.loc[index, "meli_sale_price"]
        meli_regular_price_anterior = self.df.loc[index, "meli_regular_price"]
        
            
        if meli_price > meli_regular_price_anterior:
            meli_sale_price = meli_price
            meli_regular_price = meli_price
        elif meli_price < meli_regular_price_anterior:
            meli_sale_price = meli_price
            meli_regular_price = meli_regular_price_anterior
        elif meli_price == meli_regular_price_anterior:
            meli_sale_price = meli_sale_price_anterior
            meli_regular_price = meli_regular_price_anterior     

        to_update["meli_sale_price"] = meli_sale_price
        to_update["meli_regular_price"] = meli_regular_price


        to_update["amz_site"] = self.amazon_site 
        to_update["meli_site_id"] = self.meli_site_id 
        to_update["stock_quantity"]  =   available_quantity 
        to_update["manufacturing_time"] = MANUFACTURING_TIME
        to_update["max_weigth"] = maxWeigth
        if available_quantity > 0:
            to_update["amz_status"] = 'Disponible'
        else:
            to_update["amz_status"] = 'Agotado'
            
        to_update["date_updated"] = date
        
    
        
        if (self.countryName in country or country in self.countryName or self.zip_code in country):
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
            
            #GUARDO EN MONGODB
            mongoSaveProduct(sku ,'amazon.com', self.meli_site_id, self.seller_id,  meli_sale_price, meli_regular_price, to_update["scraped_price"], available_quantity, to_update["shipping_cost"] ,to_update["taxes"] , '' , {}, '', '', self.geo_result_id )

            if (USD_total == total_price_anterior): 

                if (available_quantity == available_quantity_anterior):
                    to_update["changed"] = '--' 
                elif(available_quantity == 0):
                    to_update["changed"] = 'Agotado' 
                elif(available_quantity > available_quantity_anterior):
                    to_update["changed"] = '+ Stock'   
                elif(available_quantity < available_quantity_anterior):
                    to_update["changed"] = '- Stock' 
                # Dado que ambas se cumplen!
                print('\n @ Precio sigue igual @')
                                
                    
                print("DATA DICT TO UPDATE: ", to_update)
                for indice in buscar_index:
                    id_meli = self.df.loc[indice, "id_meli"]
                    objectDataLog = DataLogManager(self.databaseName)
                    objectDataLog.updateProducts("products_info_customers",id_meli,"id_meli", **to_update)
               
            else:
                # Si el precio cambio debo actualizar database
                print('\n @ Precio Cambio @')
                if USD_total > total_price_anterior:
                    to_update["changed"] = 'Subió'
                elif USD_total < total_price_anterior:
                    to_update["changed"] = 'Bajó'

                if (available_quantity == available_quantity_anterior) and available_quantity == 0:
                    to_update["changed"] = '--'
                elif available_quantity == 0:
                    to_update["changed"] = 'Agotado'

            
                print("DATA DICT TO UPDATE: ", to_update)
                for indice in buscar_index:
                    id_meli = self.df.loc[indice, "id_meli"]
                    objectDataLog = DataLogManager(self.databaseName)
                    objectDataLog.updateProducts("products_info_customers",id_meli,"id_meli", **to_update)
               

               
        else:
            # print('captcha o wrong country - repetir request!')
            url = f'https://www.{self.amazon_site}/-/es/dp/{str(sku)}?th=1&psc=1'
            print('captcha or error countryName, informe al administrador.')

            if 'captcha' not in self.countryName: 
                print(f'Actualizo cookie en base de datos! idcookie: {self.idcookie}')
                ''' Creo un Objeto para conexión con BaseDeDatos'''
                databaseName = 'ecommerce'
                objectDataLog = DataLogManager(databaseName)
                objectDataLog.updateCookies(self.idcookie, 'status', 'expired')
            print(f'Nuevas Cookies para sku: {sku}')
            #CAMBIOS LAS COOKIES
            self.COOKIES,self.idcookie = cookiesRefresh(0,self.seller_id,self.amazon_site,self.meli_site_id,self.zip_code)
            yield scrapy.Request(url=self.proxyFuncion(url), 
                                 callback=self.parse,  # self.proxyFuncion(url)
                                 errback=self.errback, #Manejo de errores 404 
                                 dont_filter=True,     #, meta=meta)    
                                 headers=HEADERS,
                                 cookies=self.COOKIES,
                                 cb_kwargs={'url' : url , "index": index, "idcookie":self.idcookie })

        

# the wrapper to make it run more times
@wait_for(898)
def run_spider(spider, seller_id, pack1000, quantity_pack1000):
    try:
        #print(f'run_spider: seller_id {seller_id} pack1000 {pack1000}, quantity_pack1000 {quantity_pack1000}')
        crawler = CrawlerRunner()
        d = crawler.crawl(spider, seller_id, pack1000, quantity_pack1000)
        return d
    except:
        print('Exception en run_spider dentro de autoli_dataScraper.py')
        return ''


# if __name__ == '__main__':

#     seller_id = int(sys.argv[1])  
#     pack1000 = int(sys.argv[2])

#     process = CrawlerProcess()
#     process.crawl(UpdaterSpider,seller_id,pack1000)
#     process.start()