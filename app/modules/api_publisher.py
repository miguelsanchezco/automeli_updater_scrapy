# nymeliapp v 2021.06.09
# Last updated 08/06/2021

'''
 Version automatizada de api_publicador.py
'''

# Este script realiza la publicacion de productos
# en mercadolibre a traves de la API

# Importamos Librerias de Mercadolibre y otras
# Se instalo la libreria desde github SDK Mercadolibre Python
#pip3 install git+https://github.com/mercadolibre/python-sdk.git

    
from modules.mongoCRUD import mongoSaveProduct
import json
from modules.friendlyErrMessage import friendlyErrMessage
import pandas as pd
from modules.mysqlCRUD import DataLogManager
from datetime import datetime
from random import randint
from modules.exceptions_meli import fixerr_item
from modules.cronometro import access_token_memory
from modules.apiMeliController import apiMeliController


def publisher(body,sku,description,access_token,seller_id,data_to_yield,meli_currency,databaseName,testMode): #descripcion es una lista
    
    sellerIdReal = seller_id
    site_id  = body['category_id'][:3] #MCO MLA MLM ...
    if testMode == 1:
        
        print(f'siteIdUserTest: {site_id}')
        #buscamos para el pais de la persona un usuario test
        ''' Creo un Objeto para conexión con BaseDeDatos'''
        objectDataLog = DataLogManager(databaseName)
        dataUserTest = objectDataLog.testUser(site_id)  #Test User
        seller_id_test = dataUserTest.loc[0,'seller_id']
        #print('access_token antes')
        access_token = access_token_memory(seller_id_test,databaseName)
        #print('access_token despues')
        
    path = '/tmp/'
    #path = '/tmp/'#"/data/csv/"
    nameFile = path + f'{seller_id}_response.json'

    #api_client = meli.ApiClient()

    # Usar el API_instance2 - Para hacer resquests
    #api_instance2 = meli.RestClientApi(api_client)
    
    a = 0
    contadorGTIN = 0
    while a == 0:  # PRIMER WHILE A=0 ----------------------------------------
    
        # BLOQUE TRY-EXCEPT A=0 
        # # # # # # try:
                   
        # Comunicandome con la API
        #rta = api_instance2.resource_post('/items', access_token, body)  
        response = apiMeliController('POST','items',access_token, body)
        rta = json.loads(response.text)
        # Publica Item - POST
        #print('item publicado: ',rta)
        #{'cause': [], 'message': 'Invalid token', 'error': 'not_found', 'status': 401}

        #VALIDADMOS SI FUE EXITOSO O NO
        print(f'response.status_code: {response.status_code}')
        if response.status_code > 299:
            #INVOCAR MANEJADOR DE ERRORES 
            print('rta ',rta)
            print(f"Error publicando producto: status {rta['status']}")
            if testMode == 1:
                seller_id = dataUserTest.loc[0,'seller_id'] 
            a,access_token = fixerr_item(rta,seller_id,access_token,databaseName)
            # Modulo que maneja los errores de mercadolibre 
            # publicando o actualizando item. No Descripciones.
            
            #Revision de Warning y errores
            #causas
            causes = rta['cause'] #Lista de objetos
            for cause in causes:
                if cause['type'] == 'error':
                    # # # if '[GTIN] are required' in cause['message'] and contadorGTIN<1:
                    # # #     print('GTIN es requerido, cambiar de category_id')
                    # # #     contadorGTIN = 1
                    # # #     #CREAR FUNCION QUE CAMBIA LA CATEGORIA
                    # # #     category_id =body['category_id']
                    # # #     secure = 0
                    # # #     bandera = 0
                    # # #     while secure == 0:
                            
                            
                    # # #         ruta = f'/categories/{category_id}'
                    # # #         print('ruta_Category: ',ruta)
                            
                    # # #         response = apiMeliController('GET',ruta,'','')
                    # # #         rta = json.loads(response.text)
                    # # #         status_code = (response.status_code)
                            
                    # # #         if status_code >= 500 or status_code == 429:
                    # # #             print(f'\nError {status_code}... reintentar request...\n')
                    # # #             secure = 0 # Reintentar
                    # # #             continue
                    # # #         elif status_code >299:
                    # # #             print(f'\nNuevo Error No reintentar request: {status_code}')
                    # # #             secure = 1 #todo bien
                    # # #             continue
                           

                    # # #         #print(f'Info in Categoria {rta["id"]}: {rta} ')
                    # # #         if bandera >= 1:
                    # # #             secure = 2
                    # # #             continue

                    # # #         #CAPTURAMOS LA CATEGORIA PADRE
                    # # #         path_from_root = rta['path_from_root']
                    # # #         father_category_id = rta['path_from_root'][-2]['id']
                    # # #         category_id = father_category_id
                    # # #         bandera = 1
                    # # #         print(f'bandera {bandera}. Reintentando con nueva category')
                            
                    # # #     #Ya tenemos la info de la categoria padre, buscamos un hijo Otros
                    # # #     category_otros_name = rta['children_categories'][-1]['name']
                    # # #     category_otros_id = rta['children_categories'][-1]['id']
                    # # #     data_to_yield['name_meli_category'] = category_otros_name
                    # # #     data_to_yield['id_meli_category'] = category_otros_id
                    # # #     print(f'category_otros_name : {category_otros_name}')
                    # # #     print(f'category_otros_id : {category_otros_id}')
                    # # #     # REASIGNO CATEOGORY ID 
                    # # #     body['category_id'] = category_otros_id

                    # # #     #REINTENTAR PETICION
                    # # #     a=0
                    # # #     break
                    # # # else:
                    # # #     # es otro error
                    # # #     # retornamos el error
                    # # #     #FUncion para manejar mensajes de error mas amigables al usuario
                        
                    errMessage = friendlyErrMessage(cause['message'])

                    rta['message'] = errMessage
                    a=2 
                    break

            if a == 2:

                date = str(datetime.now()).split(".")[0]
                #LEER DICCIONARIO response.json
                while True:
                    try:
                        # returns JSON object as 
                        # a dictionary
                        with open(nameFile, 'r',encoding='utf8') as file:       
                            DATA = json.load(file)
                        print(f'{date} response leido de archivo json api_publisher.py 2')
                        break
                    except Exception as e:
                        print(e)
                        continue
                
                for datica in DATA:
                    if datica['sku'] == sku:
                        datica['sku'] = sku
                        datica['id'] =  str(randint(0,9999)) + 'null'
                        datica['title'] = 'null'
                        datica['status'] = 'null'
                        datica['permalink'] = 'null'
                        datica['user_price'] = 'null'
                        datica['img'] = 'https://i.ibb.co/5W6X6vX/warning-signs-that-your-travel-expense-management-may-be-out-of-control-300x300.jpg'
                        datica['date_created'] = date 
                        datica['message'] = rta['message'] 
                        break
            
            continue    
    
        ## SI TODOESTA OK, PASA AQUI

        # ALMACENANDO DATOS DE LA RESPONSE
        date = str(datetime.now()).split(".")[0]
        
        #LEER DICCIONARIO response.json
        while True:
            try:
                # returns JSON object as 
                # a dictionary
                with open(nameFile, 'r',encoding='utf8') as file:       
                    DATA = json.load(file)
                print(f'{date} response leido de archivo json api_publisher.py 1')
                break
            except Exception as e:
                print(e)
                continue
        
        for datica in DATA:
            #print(f'sku: {sku}, => {datica}')
            if datica['sku'] == sku:
                datica['sku'] = sku
                datica['id'] = rta['id']
                datica['title'] = rta['title']
                datica['status'] = rta['status']
                datica['permalink'] = rta['permalink']
                datica['user_price'] = rta['price']
                datica['img'] = body['pictures'][0]['source']
                datica['date_created'] = date 
                datica['message'] = 'OK'
                break
        
        id_item = rta["id"]
        ruta = f'/items/{id_item}/prices/types/standard/channels/mshops'
        print(f'ruta: {ruta}')
        body_mshops = {
            
            "amount": data_to_yield['mshops_price'],
            'synced':False,
            "currency_id": meli_currency
            
        }
        try:
            #rta = api_instance2.resource_post(ruta, access_token, body_mshops) 
            response = apiMeliController('POST',ruta,access_token,body_mshops)
            rta = json.loads(response.text)
        except Exception as e:
            print(f'Error mshops: {e.body}')
            
        #Incrementamos en 1 el valor de publisher usage en base de datos
        #Verificar plan!
        credits = 1
        key = 'publisher_usage'
        if testMode == 1:
            #seller_id = dataUserTest.loc[0,'seller_id'] 
            key = 'testing_usage'
  
        ''' Creo un Objeto para conexión con BaseDeDatos'''
        objectDataLog = DataLogManager(databaseName)
        objectDataLog.usageIncrement(sellerIdReal,key,credits)  #Trae PlanInfo
        #update meli_accounts set publisher_usage = publisher_usage + 1 where seller_id= 1192172876;
        # Imprimo resultados
        print('item OK') 
        a = 1 # Item Publicado - Pasamos a publicar la Descripcion
            
           
    # FIN DEL WHILE A = 0 ---------------------------------------------

    if a == 2:
        #Error al publicar, pasar al siguiente item
        #print('No enviar descripcion, item con error')
        print('\nItem con error, No publicado\n')  
        b = 2 # para evitar errores    
    else:            
        # - D E S C R I P C I O N - 
        # - La descripcion se envia luego de publicar el item
        # - Creo ruta para postear la descripcion
        ruta = '/items/' + rta['id'] + '/description'
        # json con la descripcion
        body_description = {
            "plain_text": description[0] # item 1 de la lista
            #data['description'].replace('\\n', '\n')
            # descripcion del dataframe, sustituyendo los \\n por \n
            # Asumiendo que la description trae \n
        }
        
        b = 0

        intento = 1
        # Esta variable evita que se cree un bucle inf. en caso de que
        # la descripcion aux. tambien falle, osea presente errores.    
        
        while b == 0: # SEGUNDO WHILE B = 0 -------------------------------

            #api_instance2.resource_put(ruta, access_token, body_description)
            response = apiMeliController('PUT',ruta, access_token,body_description)
            # Posteo la descripcion del item que se acabo de publicar
            rta = json.loads(response.text)
            #print('rta description: ',rta)
            #REVISO QUE TODOESTA BIEN
            #{'message': 'The description must be in plain text', 'error': 'DESCRIPTION_PLAIN_TEXT_NOT_ALLOWED', 'status': 400, 'cause': 'item.description.type.invalid'}

            #VALIDADMOS SI FUE EXITOSO O NO
            print(f'response.status_code: {response.status_code}')
            if response.status_code > 299:
                #print('error publicando descripcion')
                print(f"\nError publicando descripcion: {rta}\n" )   
                
                # #Error Descripcion.
                if rta['status'] == 400 and intento < len(description):

                    print(f'\nError en la descripcion, Enviar Descripcion: {intento+1}\n')
                    b = 0 # Reintentar
                    # Descripcion Auxiliar
                    body_description = {
                            "plain_text": description[intento]
                    # Se tienen 7 descripciones. La original y las auxiliares 
                    }

                    #print(f'Descripcion {intento}: {description[intento]}')

                    #Con esto protegere al programa de un bucle inf.
                    intento = intento + 1

                elif rta['status'] >= 500:
                    print('\nError del Servidor... reintentar request...\n')
                    b= 0 # Reintentar
                elif rta['status'] == 429:
                    print('\nError Too Many Request... reintentar request...\n')
                    b = 0 # Reintentar
                else:
                    print(f"\nError en la descripcion: {intento}, status: {rta['status']}")
                    b = 2 # No Reintentar - las descripciones tienen muchos tipos de error
                    print('Producto Queda sin Descripcion *** Mejorar manejo de errores')
                    # objectDataLog = DataLogManager('ecommerce')  # <<<--- agregado
                    # diccionario = {'status_publication':'without_description','date_updated':date}
                    # objectDataLog.updateProducts(table, str(rta['id']), 'id_meli_publication', **diccionario)

                continue

            b = 1 # OK
            print('Descripcion OK')
            #print(body_description)


                
                
        # FIN WHILE B = 0 -----------------------------------------------

         
    while True:
            date =  str(datetime.now()).split(".")[0]
            try:
                #Guardamos        
                with open(nameFile, 'w') as file:
                #with open(f'{seller_id}.json', 'w') as file:
                    json.dump(DATA, file)
                    print(f'{date} response guardado en archivo json')
                    break
            except Exception as e:
                print(e)
                continue

    #si es testMode == 1 guardamos en base de datos  saved_products
    message = 'Producto Extraviado de una anterior ejecucion'
    print('343: sku PRODUCTO: ',sku)
    for datica in DATA:
        print('sku_datica: ', datica['sku'])
        if datica['sku'] == sku.strip():
            print('346: sku encontrado!!!: ',sku)
            idDATA = datica['id'] 
            imgDATA = datica['img']
            permalink = datica['permalink']
            message = datica['message']
            print('353: message: ',message)
            break
        # else:
        #     idDATA = datica['id'] 
        #     imgDATA = datica['img']
        #     permalink = datica['permalink']
        #     message = datica['message']

    print('362: message: ',message)     
            
    if testMode == 1 and message == 'OK':
        saved_product = {}
        saved_product['seller_id'] = sellerIdReal
        saved_product['sku'] = sku
        saved_product['img'] = imgDATA
        saved_product['user_price'] = data_to_yield['meli_price']
        saved_product['id_meli_test'] = idDATA
        saved_product['user_category_name'] = data_to_yield['name_meli_category'] ##Guardar categoria en letra
        saved_product['user_category_id'] = data_to_yield['id_meli_category'] #guardamos id category
        saved_product['listing_type_id'] = body['listing_type_id']
        saved_product['permalink'] = permalink
        saved_product['status_meli'] = 'cargando...'
        saved_product['date_created'] = date

        table_name = 'saved_products'
        while True:
            try:
                print('estoy aqui 3')
                ''' Creo un Objeto para conexión con BaseDeDatos'''
                objectDataLog = DataLogManager(databaseName)  # <<<--- agregado
                dataframe = pd.DataFrame.from_dict([saved_product])
                objectDataLog.dfToTableDB(table_name, dataframe)
                print('estoy aqui 4. SKU: ',sku)
                break
            except Exception as e:
                print(f'error guardando registro en database, reintentar. {e}')

    #Guardo en Base de Datos Producto Publicado
    elif testMode == 0 and message == 'OK':
        published_product = {}
        published_product['seller_id'] = sellerIdReal
        published_product['sku'] = sku
        published_product['image'] = imgDATA
        published_product['id_meli'] = idDATA
        published_product['title'] = body['title']
        published_product['meli_site_id'] = body['category_id'][:3]
        published_product['meli_category_name'] = data_to_yield['name_meli_category'] ##Guardar categoria en letra
        published_product['meli_category_id'] = data_to_yield['id_meli_category'] 
        published_product['create_using_publisher'] = 1
        published_product['total_price'] = data_to_yield['total_price'] 
        published_product['scraped_price'] = data_to_yield['price'] 
        published_product['shipping_cost'] = data_to_yield['shippingCost'] 
        published_product['taxes'] = data_to_yield['taxes'] 
        published_product['stock_quantity'] = data_to_yield['available_quantity'] 
        published_product['permalink'] = permalink
        published_product['meli_status'] = 'cargando...'
        published_product['date_created'] = date

        table_name = 'products_info_customers'
        while True:
            try:
                print('estoy aqui 3')
                ''' Creo un Objeto para conexión con BaseDeDatos'''
                objectDataLog = DataLogManager(databaseName)  # <<<--- agregado
                dataframe = pd.DataFrame.from_dict([published_product])
                objectDataLog.dfToTableDB(table_name, dataframe)
                print('estoy aqui 4. SKU: ',sku)
                break
            except Exception as e:
                print(f'error guardando registro en database, reintentar. {e}')

        #GUARDO TAMBIEN EN MONGODB
        mongoSaveProduct(sku ,'amazon.com', site_id, seller_id,  data_to_yield['meli_price'], data_to_yield['price'] ,data_to_yield['available_quantity'], data_to_yield['shippingCost'] ,data_to_yield['taxes'], body['title'] , body['pictures'], data_to_yield['id_meli_category'], body['currency_id'] )

# NOTAS DE LA VERSION 08/06/2021
'''
Ultima Actualizacion 05 de Junio de 2021
Si el producto se publica sin descripcion, se envia un mensaje a la base de 
datos, posteriormente se debe crear un modulo que actualice esos productos.
'''
# NOTAS DE LA VERSION 05/06/2022
'''
    Todo OK 2022
'''