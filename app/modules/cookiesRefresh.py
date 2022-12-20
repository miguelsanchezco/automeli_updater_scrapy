import json
import os
from modules.cookiesGenerator import cookiesGenerator, cookiesFromDB

def cookiesRefresh(index,seller_id,amazon_site,meli_site,zip_code):
    
    print('COOKIES REFRESH')
    if (index)%1000 == 0 or index == 0:
        # Recalcular Cookies
        print(f'Recalculando cookies {index} - Multiplo de 1000 ')
        
        #COOKIES = cookiesGenerator(amazon_site, meli_site, zip_code, seller_id) #este guarda cookies en json
        COOKIES,idcookie = cookiesFromDB(amazon_site, meli_site, zip_code, seller_id)
        print(f'cookieID:: {idcookie} cookiesRefresh')
    else:
        idcookie = 100000
        print(f'leemos cookies json: {index}')
        #path = os.getcwd() +'/tmp/'
        path = '/tmp/'
        try:

            with open(path + f'{seller_id}.json', 'r') as file:       
                COOKIES = json.load(file)
                print(f'Si existe cookies: {COOKIES}')
                
        except FileNotFoundError as e:

            print(f'No Existe cookies anterior, la definimos! {e}')
            COOKIES = cookiesGenerator(amazon_site, meli_site, zip_code, seller_id) #este guarda cookies en json
    
    return COOKIES,idcookie