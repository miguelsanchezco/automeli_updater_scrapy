
import random
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import json
import pandas as pd

#from mysqlCRUD import DataLogManager 
from modules.mysqlCRUD import DataLogManager 
#from randomScraperApiKey import randomScraperApiKey
from modules.randomScraperApiKey import randomScraperApiKey

def cookiesGenerator(amazon_site, meli_site, zip_code, seller_id):

    if meli_site == 'MLM':
        countryCode = 'MX' 
        countryName = 'México Mexico'
    elif meli_site == 'MCO':
        countryCode = 'CO'
        countryName = 'Colombia'
    else:
        countryCode = 'US'
        countryName = 'address dirección'

    if amazon_site == 'amazon.com':
        BaseURL = "http://www.amazon.com/"
        if meli_site != '':
            locationType = 'COUNTRY'
        else:
            #Para personas que estan en Estados Unidos
            locationType = 'LOCATION_INPUT' #ZipCode

    elif amazon_site == 'amazon.com.mx':
        BaseURL = "http://www.amazon.com.mx/" 
        
        if meli_site == 'MLM':
            #Para personas en Mexico, pueden usar ZipCode o CP
            locationType = 'LOCATION_INPUT' #CP
        
        else:
            #Personas en otro pais
            locationType = 'COUNTRY'

    if locationType == 'COUNTRY':
        #POR PAIS
        payload=f'locationType=COUNTRY&district={countryCode}&countryCode={countryCode}&storeContext=generic&deviceType=web&pageType=Gateway&actionSource=glow&almBrandId=undefined'
    elif locationType == 'LOCATION_INPUT' :
        #POR ZIPCODE - VALIDO PARA USA O MX
        payload=f'locationType=LOCATION_INPUT&zipCode={zip_code}&storeContext=generic&deviceType=web&pageType=Gateway&actionSource=glow&almBrandId=undefined'
    
    date =  str(datetime.now()).split(".")[0]
    print(f'{date}countryCode: {countryCode}, countryName: {countryName}, meli_site: {meli_site}, amazon_site:{amazon_site}, zip_code: {zip_code}')
    
    headers = {
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

    contador = 0
    
    while True:

        try:
            date =  str(datetime.now()).split(".")[0]
            print(f'\nFecha cookies: {date}')
            contador  = contador +1
            print(f'{date} contador: {contador}')

            
        
            #curl -x "http://scraperapi:d953019d893d570c75ab356c8a218a12@proxy-server.scraperapi.com:8001" -k "http://httpbin.org/ip"
            sessionNumber = random.randint(0,1000)
            if contador <= 5:
                
                #API_KEY = '3b123199c0a17c7fe514baf06c341528'
                API_KEY = randomScraperApiKey()
                proxy = { 'https': f'http://scraperapi.keep_headers=true&session_number={sessionNumber}:{API_KEY}@proxy-server.scraperapi.com:8001'}
            
            else:
                
                API_KEY = 'fa92d233f85e48889c92df47248b944dc7242844c54'
                date =  str(datetime.now()).split(".")[0]
                print(f'{date} PROXY SCRAPE.DO')
            
                proxy = { 'https':f'http://{API_KEY}:customHeaders=true&sessionId={sessionNumber}@proxy.scrape.do:8080'}
                #'http':f'http://{API_KEY}:customHeaders=true&sessionId={sessionNumber}@proxy.scrape.do:8080'
                if contador > 10:
                    contador = 0 #Reiniciamos Contador

            s =  requests.session()



            ###############################################################

            print('\n\nParte 1. Request a Amazon - Obtenemos anti-csrftoken-a2z (1)')

            response = s.get( BaseURL, proxies=proxy, verify=False,headers=headers, timeout=20)
            
            print('status_code cookies:',response.status_code)
            #support@scraperapi.com
            if response.status_code != 200:
                date =  str(datetime.now()).split(".")[0]
                print(f'{date} cambiarApiKey status_code cookies: {response.status_code}')
                #sessionNumber = random.randint(0,1000)
                #print('sessionNumber:',sessionNumber)
                #API_KEY = '3b123199c0a17c7fe514baf06c341528'
                #API_KEY = randomScraperApiKey()
                #curl -x "http://scraperapi:d953019d893d570c75ab356c8a218a12@proxy-server.scraperapi.com:8001" -k "http://httpbin.org/ip"
                #proxy = { 'https': f'http://scraperapi.keep_headers=true&session_number={sessionNumber}:{API_KEY}@proxy-server.scraperapi.com:8001'}
                continue


            soup = BeautifulSoup(response.text, 'lxml')
            country = soup.find("div", {"id":"glow-ingress-block"})
            date =  str(datetime.now()).split(".")[0]
            if country:
                country = country.find("span", {"class":"nav-line-2"}).text.strip()
                
                print(f'\nFecha: {date}, country ScraperAPI: {country}, sessionN: {sessionNumber}, ApiK: {API_KEY}')
                #SI NO ENCUENTRA PAIS! REINICIAR
            else:
                
                print(f'\nFecha: {date}, country ScraperAPI: None, sessionN: {sessionNumber}, ApiK: {API_KEY}')
                print('Reiniciando ...')
                continue

            #Obtener csrf token 1 -----------------------------------------
            soup = BeautifulSoup(response.text, 'lxml')
            csrfToken1 = soup.find("input", {"id":"glowValidationToken"})
            if csrfToken1:
                csrfToken1  =  csrfToken1['value'] 
                print('\ncsrfToken1: ', csrfToken1)
                headers['anti-csrftoken-a2z'] = csrfToken1
            else:
                print('Reiniciando ...')
                continue
                

            #time.sleep(1)
            ###############################################################
            #Crear tokens de session
            url = f"{BaseURL}ah/ajax/counter?ctr=desktop_ajax_atf&exp=1658767496405&rId=9DPATZPJ0T0BE6RQC880&mkId=ATVPDKIKX0DER&h=b18befedcf2f6c034967e97656d5c09714fd81c5e049443b4dcc7bca50f0aceb"

            print('\n\nParte 2. Obtenemos tokens de session Cookie')

            response = s.get( url,  headers=headers)

            # print('\nheaders request: ', response.request.headers)
            # print('\ncookies response: ', response.cookies) 
            # print('\nheaders response: ', response.headers)

            #time.sleep(1)
            ###############################################################
            #CSRF TOKEN 2
            print('\n\nParte 3. Obtenemos anti-csrftoken-a2z (2) ')

            url = f"{BaseURL}portal-migration/hz/glow/get-rendered-address-selections?deviceType=desktop&pageType=Gateway&storeContext=NoStoreName&actionSource=desktop-modal"

            response = s.get( url, proxies=proxy, verify=False, headers=headers, timeout=20)
            #Obtener csrf token 2
            # soup = BeautifulSoup(response.text, 'lxml')
            # csrfToken1 = soup.find("input", {"id":"glowValidationToken"})['value']
            parte1 = response.text.split('CSRF_TOKEN :')
            date =  str(datetime.now()).split(".")[0]
            if parte1:
                #Revisamos si trae el CSRF token
                if len(parte1)>1:
                    #Si lo tae!
                    parte1 = parte1[1]
                    ncsrfToken2 = str(parte1.split(',')[0].strip().replace('"',''))
                    print('\ncsrfToken2:',ncsrfToken2)
                    headers['anti-csrftoken-a2z'] = ncsrfToken2
                else:
                    #No tiene el CSRF token
                    print(f'{date} Reintentando...')
                    continue
            else:
                #NoneType
                print(f'{date} Reintentando...')
                continue
            # time.sleep(1)
            ###############################################################

            #Paso 5. Cambiar Pais
            print('\n\nParte 4. Cambiamos de Pais')
            
            url = f"{BaseURL}gp/delivery/ajax/address-change.html"

            response = s.post( url, headers=headers, proxies=proxy, verify=False, data=payload, timeout=20)
            #response = requests.request("POST", url, headers=headers, data=payload)

            # print('\nresponse.text ',response.text)
            # print('\nheaders request: ', response.request.headers)
            # print('\ncookies response: ', response.cookies) 
            # print('\nheaders response: ', response.headers)

            #time.sleep(1)
            ###############################################################
            print('\n\nParte 5. Verificamos el cambio de Pais, extraemos cookies')


            #response = s.get( BaseURL,proxies=proxy, verify=False, headers=headers)
            response = s.get( BaseURL, headers=headers)

            # print('\nheaders request: ', response.request.headers)
            # print('\ncookies response: ', response.cookies) 
            # print('\nheaders response: ', response.headers)

            soup = BeautifulSoup(response.text, 'lxml')
            country = soup.find("div", {"id":"glow-ingress-block"})
            date =  str(datetime.now()).split(".")[0]
            if country:
                country = country.find("span", {"class":"nav-line-2"}).text.strip()
                print(f'\n{date} country Verification: {country}')
                #SI NO ENCUENTRA PAIS! REINICIAR
            else:
                print('Reiniciando ...')
                continue

            if country in countryName or countryName in country or zip_code in country:
                print('Pais Correcto! Successfully!')    
            else:
                print('Pais o ZipCode Equivocado... Reintentando...')
                continue

            print('\ncookies to save: ', response.request.headers['Cookie'])
            cookies = response.request.headers['Cookie']
            
            #######################################################
            #Guardando
            print('\nPaso 6. Convertir cookies en Dict')

            from http.cookies import SimpleCookie
            cookie = SimpleCookie()
            cookie.load(cookies)
            cookies = {}
            for key, morsel in cookie.items():
                cookies[key] = morsel.value
            print('\ncookies Dict: ',cookies)
            currency = cookies['i18n-prefs']
            print('moneda:',currency)

            ''' Creo un Objeto para conexión con BaseDeDatos'''
            objectDataLog = DataLogManager("ecommerce")  
            table = 'cookies'
            dictJson = {} 
            stringCookies = json.dumps(cookies) #convierto dict en json 
            now_now = str(datetime.now()).split('.')[0] #Fecha y Hora 2021-06-22 15:25:12
            dictJson['cookie_json'] = [stringCookies]
            dictJson['amazon_site'] = [amazon_site]
            dictJson['meli_site'] = [meli_site]
            dictJson['zip_code'] = [zip_code]
            dictJson['date_created'] = [now_now]
            df = pd.DataFrame(dictJson)
            objectDataLog.dfToTableDB(table, df)

            # while True:
            #     #Guardamos las cookies
            #     try: 
            #         with open(f'data/json/cookies/{seller_id}.json', 'w') as file:
            #             json.dump(cookies, file)
            #             date =  str(datetime.now()).split(".")[0]
            #             print(f'{date} cookies guardadas en archivo json')
            #             break
            #     except Exception as e:
            #         print(e)
            #         continue

            #break
        
        except Exception as error:
            date =  str(datetime.now()).split(".")[0]
            print(f'{date} Ups! Error en Cookies: {error}')
            print(f'{date} Reiniciando cookiesGenerator: BUG SOLVED')
            contador = 0
            continue

    #return cookies

def cookiesFromDB(amazon_site, meli_site, zip_code, seller_id):
    ''' Creo un Objeto para conexión con BaseDeDatos'''
    objectDataLog = DataLogManager("ecommerce")
    cookiesDf = objectDataLog.downloadCookies(amazon_site, meli_site, zip_code)
    cookies = json.loads(cookiesDf['cookie_json']) #convierto json-string en dict
    #path = os.getcwd() +'/tmp/'
    path = '/tmp/'
    while True:
            #Guardamos las cookies
            try:
                with open(path + f'{seller_id}.json', 'w') as file:
                #with open(f'{seller_id}.json', 'w') as file:
                    json.dump(cookies, file)
                    date =  str(datetime.now()).split(".")[0]
                    print(f'{date} cookies guardadas en archivo json')
                    break
            except Exception as e:
                print(e)
                continue

    return cookies,cookiesDf['idcookie']

if __name__ == '__main__':
    
    seller_id = '116499542'
    amazon_site  = 'amazon.com'
    meli_site = 'MCO'
    zip_code = '00000'

    cookiesFromDB(amazon_site, meli_site, zip_code, seller_id)
    #cookiesGenerator(amazon_site, meli_site, zip_code, seller_id)