'''
    . Automeli Products Scraper 
    - nymeliapp_DataSpider.py
    . Last updated: 13/08/2021
    . Description: This spider,extract product's data from amazon,
    . this data is local procesed and finally save in a database.
    . After this data is published in meli using meli web api.
    . Programmer: Miguel Angel Sanchez Ramirez
    . Instagram: @miguelsanchezco
    . Twitter: @miguesanchezco
    . Requirements:
      scrapy, meli (github repository)
      own modules like: cronometro (access_token), selector_css (selectors), 
      google_sheets (API Google Sheets), exceptions_meli
'''
from crochet import setup, wait_for
from scrapy.crawler import CrawlerRunner
#Librerias
# from scrapy.crawler import CrawlerProcess 
import scrapy
# # import scrapy.crawler as crawler

# # from multiprocessing import Process, Queue
# # from twisted.internet import reactor
import json
from urllib.parse import urlencode
from datetime import datetime

from modules.priceFactorsConversion import priceFactorsConversion
from modules.api_atributos import api_atributos

# Modulos Propios
from publish_items_meli import publishInMeli
from modules.cookiesRefresh import cookiesRefresh
from modules.selectores_css2 import selectores_css2
from modules.selectores_css import selectores_css
from modules.api_imagenes_json import img_depuration
from modules.titleCreator import titleCreator
from modules.attr_amazon import attr_amazon
from modules.mysqlCRUD import DataLogManager

# Imports para manejo de errores 400 
from scrapy.spidermiddlewares.httperror import HttpError
from os import remove

#path = os.getcwd() + '/tmp/'
path = '/tmp/'
nameFile = path + str(datetime.now()).split(' ')[0] + '_fulldata_.json'
try:
    remove(nameFile)
except:
    pass

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

# Declaramos una Clase spider
class ScrapeDataProduct(scrapy.Spider):

    # Atributos
    test_mode = ''
    access_token = ''
    listing_type_id = ''
    dataUser = ''
    user_category_id = ''
    name = 'scrape_data'
    databaseName = 'ecommerce_prueba'
    seller_id = ''
    amazon_site  = ''
    meli_site_id = ''
    zip_code = '00000'
    mtauto = ''
    mtactive = ''
    mtdays = ''
    use_locker = 0
    skus = []
    titles = []
    trm = ''
    meli_currency = ''
    countryName = ''
    idcookie = ''
    COOKIES = {}

    # Configuraciones
    custom_settings = {
        # 'FEED_URI' : nameFile, 
        # 'FEED_FORMAT' : 'json',
        # 'FEED_EXPORT_ENCODING': 'utf-8',
        # 'FEED_OVERWRITE': True,
        'CONCURRENT_REQUESTS' : 2, #ScraperAPI  
        'RETRY_TIMES': 4, # ScraperAPI Recommendation
        'ROBOTSTXT_OBEY' : False,
        'CONCURRENT_REQUESTS_PER_IP' : 2 #ScraperAPI        
    }
  

    def __init__(self, skus=[], seller_id='', user_category_id='', listing_type_id='', access_token='',test_mode='',titles=[],*args, **kwargs):
        super(ScrapeDataProduct, self).__init__(*args, **kwargs)

        print(f"skus: {skus} seller_id: {seller_id}")
        self.skus = skus 
        self.seller_id = seller_id
        self.user_category_id = user_category_id
        self.listing_type_id = listing_type_id
        self.access_token = access_token
        self.test_mode = test_mode
        self.titles = titles
        print('self.titles: ',self.titles)

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
        self.use_locker =  int(self.dataUser.loc[0,'use_locker'])
        self.meli_currency = self.dataUser.loc[0,'meli_currency']
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
        #Scrape.do
        API_KEY ='c2beda536e3f48bb9ededf793f4e6b0bf32639f621a'

        payload = {'token': API_KEY, 
                   'url': url,
                   'customHeaders':'true'}
                   #'geoCode': COUNTRY_CODE}

        proxy_url = 'http://api.scrape.do/?' + urlencode(payload)
        return proxy_url



    def start_requests(self):
        
        # urls = [f'https://www.{self.amazon_site}/-/es/dp/{self.sku}?th=1&psc=1']
        self.COOKIES,self.idcookie = cookiesRefresh(0,self.seller_id,self.amazon_site,self.meli_site_id,self.zip_code)

        for index, sku in enumerate(self.skus):
            sku = sku.strip()
            url = f'https://www.{self.amazon_site}/-/es/dp/{sku}?th=1&psc=1'
            print(f'URL : {url}')
            print(f'cookieID:: {self.idcookie}')
            yield scrapy.Request(url=self.proxyFuncion(url), 
                                    callback=self.parse,  #, meta=meta)  self.get_scraperapi_url(url)
                                    errback=self.errback, #Manejo de errores 400 
                                    dont_filter=False,
                                    headers=HEADERS,
                                    cookies=self.COOKIES,
                                    cb_kwargs={'variante':False, 'parent_sku':sku, 'url':url, 'idcookie':self.idcookie,'index':index})     #self.proxyfuncion(url)
    
    ### Funcion para manejo de errores 400
    # Fuente: https://docs.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-errbacks
    def errback(self, failure):

        # log all failures
        self.logger.error(repr(failure))
        index = failure.request.cb_kwargs['index']
        url = failure.request.cb_kwargs['url']
        sku = failure.request.cb_kwargs['parent_sku']
        variante = failure.request.cb_kwargs['variante']
        idcookie = failure.request.cb_kwargs['idcookie']

        if failure.check(HttpError):

            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            print(f'status_code: {response.status}')
            
            if response.status == 404:  
                ##################################################################################
                path = '/tmp/'
                nameFile = path + f'{self.seller_id}_response.json'
                #LEER DICCIONARIO response.json
                while True:
                    try:
                        # returns JSON object as 
                        # a dictionary
                        with open(nameFile, 'r',encoding='utf8') as file:       
                            DATA = json.load(file)
                        #print(f'{date} response leido de archivo json')
                        break
                    except Exception as e:
                        print(e)
                        continue
                
                for datica in DATA:
                    if datica['sku'] == sku:
                        datica['message'] = f'Producto No Existe en Amazon.com'
                
                while True:
                    
                    try:
                        #Guardamos        
                        with open(nameFile, 'w') as file:
                        #with open(f'{seller_id}.json', 'w') as file:
                            json.dump(DATA, file)
                            #print(f'{date} response guardado en archivo json')
                            break
                    except Exception as e:
                        print(e)
                        continue

            elif response.status >= 400 and response.status < 500:
                #Reintentar requests
                #COOKIES = cookiesRefresh(index,self.seller_id,self.amazon_site,self.meli_site_id,self.zip_code)
                print(f'ERROR {response.status} - Reintentar request \n')
                yield scrapy.Request(url=self.proxyFuncion(url),#self.get_scraperapi_url(url)
                                    callback=self.parse,
                                    errback=self.errback, #Manejo de errores 
                                    dont_filter=True,
                                    headers=HEADERS,
                                    cookies=self.COOKIES,
                                    cb_kwargs={'variante':variante, 'parent_sku':sku, 'url':url, 'idcookie':idcookie, 'index':index})#, meta=meta)
        

    # Metodo Parse - Importante
    def parse(self, response, **kwargs):

        
        try:
            index = kwargs['index']
            userTitle = self.titles[index]
        except:
            userTitle = 'vacio'

        print('index: ', index)
        print('userTitle: ',userTitle)    
        # country , Geolocalizacion 
        try:
            country = response.css('span#glow-ingress-line2::text').get().replace("\n","")
        except:
            country = 'null'

        if country:
            country = country.replace('\u200e','').replace('\t', '').replace('  ','')
            print(f'Country:{country}\n')

        #print(f'self.countryName:{self.countryName}')
        #if  not(self.countryName in country or self.zip_code in country): 
        #soyVariante = False
        #
        #print('\n\nFUNCION PARSE! UNA VARIANTE AQUI!!!')
        soyVariante = kwargs['variante'] #True or False
        #parent_sku = kwargs['parent_sku']
        idcookie = kwargs['idcookie']
        print(f'idcookie kwargs: {idcookie}')
            #true, si es una variante
            #entonces, no debo scrapear las variantes de nuevo
        #
        
        data_to_yield = {} # Para exportar archivo csv. con la data
        now_now = str(datetime.now()).split('.')[0] #Fecha y Hora 2021-06-22 15:25:12
        print(f'\nDATE: {now_now}')
        data_to_yield['created_at'] = now_now
        # Atencion: SI cambio el metodo usado de ScraperAPI - API, PROXY, SDK debo tener
        # cuidado con la siguiente instruccion de extraer el SKU, puede producir error
        try:
            #sku = (((urlparse(response.request.url).path).split('/dp/')[1]).split('/'))[0]  # Sin ScraperAPI
            sku = (response.request.url).split('dp%2F').pop().split('%2F')[0].split('%3F')[0] # Metodo API, scraperapi
            #sku = (response.request.url).split('%2F').pop().split('&')[0]  # ScraperAPI with country_code
            print(f'SKU: {sku}')
        except:
            # si error, muestro mensaje e intento obtener el sku por el metodo 2.
            print("Error extrayendo el SKU de la response, verifica si cambiaste el metodo de conectar a ScraperAPI, la url cambia.")
            
        # Extrae SKU de la url de request
        data_to_yield['sku'] = sku
        #print(f'SKU: {sku}')
        
        # SELECTORES CSS 2
        amzn_category, brand, modelo, nReviews, score = selectores_css2(response)
        #print(f'Categoria: {categoria}')

        #Caracteristicas obtenidas en el modulo attr_amazon
        attributesTable,attributesDict  = attr_amazon(response)
        print(f'ATRIBUTOS DICT AMZN: {attributesDict}')
        title = titleCreator(response,attributesTable,brand,amzn_category,modelo,userTitle)
        
        data_to_yield['title'] = title.strip()  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Extrae las iamgenes del html usando expresiones regulares
        # Modulo imagenes img, crea el json para enviar a mercadolibre
        data_to_yield,list_images = img_depuration(data_to_yield,response) #data_to_yield, response  !!!!
        
        #.pfDescContent > div:nth-child(1) > p:nth-child(1)
        #.aok-offscreen
        # DESCRIPCIONES #
        parrafo = response.css('div.a-spacing-medium.a-spacing-top-small ul span::text').getall()
        #parrafo3 = response.css('.aok-offscreen').getall()
        #parrafo3 = response.css('h3.product-facts-title span')
        #print(f'parrafo3 {parrafo3}')
        # Descripcion del producto, se crea una lista
        parrafo2 = response.css('#productDescription p span::text').getall()    
        if len(parrafo2) == 0:
            parrafo2 = response.css('#productDescription .a-list-item > span::text').getall()
            if len(parrafo2) == 0:
                parrafo2 = response.css('div#productDescription p::text').getall()
                if len(parrafo2) == 0:
                    parrafo2 = response.css('div#productFactsDesktopExpander ul li span::text').getall()    
                    if len(parrafo2) == 0:
                        parrafo2 = ''

        texto = ''
        for linea in parrafo:
            #Concatenamos los items de la lista en un solo string
            texto = texto + linea.strip() + ('\n')
        texto = texto.replace('\n \n','\n').replace('\n\n','\n').replace('al ingresar tu número de modelo.','').strip()
        texto = texto.replace('\n','\n\n').replace('www','').replace('Amazon','---').replace('https://','').replace('.com','').replace('amazon','---')

        texto2 = ''
        for linea in parrafo2:
            #Concatenamos los items de la lista en un solo string
            texto2 = texto2 + linea.strip() + ('\n')
        texto2 = texto2.replace('\n \n','\n').replace('\n\n','\n').replace('al ingresar tu número de modelo.','').strip()
        texto2 = texto2.replace('\n','\n\n').replace('www','').replace('Amazon','---').replace('https://','').replace('.com','').replace('amazon','---')

        if texto == None or texto == '' or texto == ' ':
            texto = ''
        if texto2 == None or texto2 == '' or texto2 == ' ':
            texto2 = ''
        # DESCRIPCIONES #


        ## COLOR VARIANTE:
        color = response.css('.a-section.a-spacing-small .a-row .selection::text').get()
        if color == None:
            color = response.css('span.selection::text').get()
            if color == None:
                color == 'color'
        

       
        maxWeigth = 0
        [scraped_price,available_quantity,MANUFACTURING_TIME,weight,volume,pesoVol,maxWeigth,
        USD_total,country,vendedor,despachador,shippingCost,taxes] = selectores_css(response,maxWeigth,self.mtactive,self.mtauto,self.mtdays,self.use_locker,self.meli_site_id)

        meli_price, mshops_price =  priceFactorsConversion(USD_total,self.seller_id,self.databaseName,self.meli_site_id)

        id_meli_category,name_meli_category,body_attr = api_atributos(title,sku,attributesDict,brand,modelo,weight,amzn_category,self.meli_site_id,self.user_category_id)

        # # # # sku_variantes = []
        # # # # sku_variantes = response.css('li::attr(data-defaultasin)').getall()
        # # # # if sku_variantes != []:
        # # # #     have_variants = 'true'
        # # # # else:
        # # # #     have_variants = 'false'
       
        if soyVariante == False: #and maxWeigth <= 40: #No es una variante
            #print('\n\n YIELD DE UNA PRINCIPAL!!!!')
            data_to_yield['amzn_currency'] = self.COOKIES['i18n-prefs']
            data_to_yield['total_price'] = USD_total
            data_to_yield['price'] = scraped_price
            data_to_yield['shippingCost'] = shippingCost
            data_to_yield['taxes'] = taxes
            data_to_yield['meli_currency'] = self.meli_currency
            data_to_yield['meli_price'] = meli_price
            data_to_yield['mshops_price'] = mshops_price
            data_to_yield['country_data'] = country
            data_to_yield['available_quantity'] = available_quantity
            data_to_yield['manufacturing_time'] = MANUFACTURING_TIME
            data_to_yield['amzn_category'] = amzn_category
            data_to_yield['id_meli_category'] = id_meli_category
            data_to_yield['name_meli_category'] = name_meli_category
            data_to_yield['product_seller'] = vendedor
            data_to_yield['product_shipped_from'] = despachador
            data_to_yield['maxWeigth'] = maxWeigth
            data_to_yield['dimensions'] = volume
            data_to_yield['brand'] = brand
            data_to_yield['model'] = modelo
            data_to_yield['amzn_attributes'] = attributesDict
            #data_to_yield['have_variants'] = have_variants
            #data_to_yield['parent_sku'] = parent_sku
            data_to_yield['description_1'] = texto 
            data_to_yield['description_2'] = texto2 
            #data_to_yield['reviews_number'] = nReviews
            #data_to_yield['score'] = score
            data_to_yield['color'] = color.strip() if color != None else 'null'
            #data_to_yield['INFRINGE_POLITICAS'] = veredicto
            #data_to_yield['EVIDENCIA'] = evidencia
            data_to_yield['meli_attributes'] = body_attr
            
            #if variantes != []:
            #yield data_to_yield
            print(f'countryEsperado:{self.countryName}, countryCookies:{country}')
            if (self.countryName in country or country in self.countryName or self.zip_code in country):
                ''' Creo un Objeto para conexión con BaseDeDatos'''
                print(f'cookieID:: {idcookie} en Spider')
                databaseName = 'ecommerce'
                objectDataLog = DataLogManager(databaseName)
                objectDataLog.updateCookies(idcookie, 'status', 'OK')
                publishInMeli(data_to_yield,self.seller_id,self.databaseName,self.dataUser,self.listing_type_id,self.access_token,self.test_mode)
            
            else:
                
                print('error countryName, informe al administrador.')
                ''' Creo un Objeto para conexión con BaseDeDatos'''
                databaseName = 'ecommerce'
                objectDataLog = DataLogManager(databaseName)
                objectDataLog.updateCookies(self.idcookie, 'status', 'expired')
                
                path = '/tmp/'
                #path = '/tmp/'#"/data/csv/"
                nameFile = path + f'{self.seller_id}_response.json'
                #LEER DICCIONARIO response.json
                while True:
                    try:
                        # returns JSON object as 
                        # a dictionary
                        with open(nameFile, 'r',encoding='utf8') as file:       
                            DATA = json.load(file)
                        #print(f'{date} response leido de archivo json')
                        break
                    except Exception as e:
                        print(e)
                        continue
                
                for datica in DATA:
                    if datica['sku'] == sku:
                        datica['message'] = f'Error de Geolocalización, Por favor Reintenta la solicitud'
                
                while True:
                    date =  str(datetime.now()).split(".")[0]
                    try:
                        #Guardamos        
                        with open(nameFile, 'w') as file:
                        #with open(f'{seller_id}.json', 'w') as file:
                            json.dump(DATA, file)
                            #print(f'{date} response guardado en archivo json')
                            break
                    except Exception as e:
                        print(e)
                        continue
            # # # if pasada == 1:
            # # #     for variante in sku_variantes:
            # # #         if variante != "" and variante != sku:
            # # #             print(f"\n\nVARIANTEEEEEEEEEEEE: {variante}")
            # # #             url = 'https://amazon.com/-/es/dp/' + str(variante) + '/'
            # # #             yield scrapy.Request(url=self.proxyFuncion(url), 
            # # #                             callback=self.parse,  #, meta=meta)  self.get_scraperapi_url(url)
            # # #                             errback=self.errback, #Manejo de errores 400 
            # # #                             dont_filter=False,
            # # #                             cb_kwargs={'variante':True, 'parent_sku':sku, 'url':url})
            # # # elif pasada == 2:
            # # #     pass


        # # # # else: #elif maxWeigth <= 40:
        # # # #     #Si es una variante
        # # # #     #data_to_yield['category_id'] = category_id
        # # # #     print('\n\n YIELDDD DE UNA VARIANTE **')
        # # # #     data_to_yield['usd_total'] = USD_total
        # # # #     data_to_yield['usd'] = scraped_price
        # # # #     data_to_yield['shippingCost'] = shippingCost
        # # # #     data_to_yield['taxes'] = taxes
        # # # #     data_to_yield['meli_price'] =  meli_price
        # # # #     data_to_yield['mshops_price'] =  mshops_price
        # # # #     data_to_yield['country_data'] = country
        # # # #     data_to_yield['available_quantity'] = available_quantity
        # # # #     data_to_yield['manufacturing_time'] = MANUFACTURING_TIME
        # # # #     data_to_yield['amzn_category'] = amzn_category
        # # # #     data_to_yield['id_meli_category'] = id_meli_category
        # # # #     data_to_yield['name_meli_category'] = name_meli_category
        # # # #     data_to_yield['product_seller'] = vendedor
        # # # #     data_to_yield['product_shipped_from'] = despachador
        # # # #     data_to_yield['maxWeigth'] = maxWeigth
        # # # #     data_to_yield['dimensions'] = volume
        # # # #     data_to_yield['brand'] = brand
        # # # #     data_to_yield['model'] = modelo
        # # # #     data_to_yield['amzn_attributes'] = attributesDict
        # # # #     data_to_yield['have_variants'] = have_variants
        # # # #     data_to_yield['parent_sku'] = parent_sku
        # # # #     data_to_yield['description_1'] = texto 
        # # # #     data_to_yield['description_2'] = texto2 
        # # # #     data_to_yield['reviews_number'] = nReviews
        # # # #     data_to_yield['score'] = score
        # # # #     data_to_yield['color'] = color.strip() if color != None else 'null'
        # # # #     #data_to_yield['INFRINGE_POLITICAS'] = veredicto
        # # # #     #data_to_yield['EVIDENCIA'] = evidencia
        # # # #     data_to_yield['meli_attributes'] = body_attr
        # # # #     #if variantes != []:
        # # # #     #yield data_to_yield
        
# the wrapper to make it run more times
@wait_for(27)
def run_spider(spider, skus, seller_id, user_category_id, listing_type_id,access_token,test_mode,titles):
    try:
        crawler = CrawlerRunner()
        d = crawler.crawl(spider, skus, seller_id, user_category_id, listing_type_id,access_token,test_mode,titles)
        return d
    except:
        print('Exception en run_spider dentro de autoli_dataScraper.py')
        return ''
    # # # def f(q):
    # # #     try:
    # # #         runner = crawler.CrawlerRunner()
    # # #         deferred = runner.crawl(spider, skus, seller_id, user_category_id, listing_type_id)
    # # #         deferred.addBoth(lambda _: reactor.stop())
    # # #         reactor.run()
    # # #         q.put(None)
    # # #     except Exception as e:
    # # #         q.put(e)

    # # # q = Queue()
    # # # p = Process(target=f, args=(q,))
    # # # p.start()
    # # # result = q.get()
    # # # p.join()

    # # # if result is not None:
    # # #     raise result

# # if __name__ == "__main__":

# #     print('hola Mundo Inicio')
# #     seller_id = '116499542'
# #     sku = 'B01HXP3VFK' 
# #     process = CrawlerProcess()
# #     process.crawl(ScrapeDataProduct, sku=sku, seller_id = seller_id)
# #     process.start()
# #     print('hola Mundo Fin')


# # # NOTAS ULTIMA VERSION 14/08/2021

# QUEDA PENDIENTE REALIZAR ANALISIS MEDIANTE REGEX A
# LA DESCRIPCION Y AL TITULO, ATRIBUTOS, EN BUSCA DE PALABRAS
# PROHIBIDAS, MARCAS O DATOS DE CONTACTO.
# REFURBISHED, REACONDICIONADO, ADIDAS, NIKE, MICROSOFT
# USADO, AMAZON.COM ...

# SE DEBE ARREGLAR LA DESCRIPCION CON LOS ATRIBUTOS ***
# SE DEBE MEJORAR EL MODULO QUE RELLENA LOSA ATRR 
# REQUERIDOS POR MELI. SE ENCONTRO UNA FALLA CUANDO
# HAY MUCHOS DEL TIPO SI/NO Y SE ENVIABAN TODOS COMO N/A
# MELI SE DABA CUENTA Y BAJABA LA EXPOSICION.

# BORRAR EN LA DESCRIPCION DE LOS PRODUCTOS LA PARTE QUE
# DICE PREGUNTAR POR DISPONIBILIDAD  Y PRECIO!
# INFRINGE LAS NORMAS