# nymeliapp v 2021.06.09
# Modulo api_atributos!
# Predictor de categorias + llenado de atributos
# Miguel Sanchez
# 31/05/2021 inicio programacion.

# Importamos Librerias
#from os import access
#import meli 
#from meli.rest import ApiException
from modules.attrMeliLogic import attrMeliLogic
from modules.apiMeliController import apiMeliController
import json


# api_client = meli.ApiClient()
# api_instance2 = meli.RestClientApi(api_client)

#access_token = 'APP_USR-536427975267539-052620-8b5b5ac72b5f43306ac0d269e3f2a4bf-116499542'

def api_atributos(title,sku,attributesDict,brand,model,weigth,amzn_category,meli_site_id,user_category_id):

    # PREDICCION CATEGORIA
    #Este trozo de codigo se encarga de hacer la request a mercadolibre
    #para obtener la Prediccion de la categoria del porducto consultado.

    #ruta = f'/sites/{meli_site_id}/domain_discovery/search?limit=1&q=' + amzn_category + ' ' + user_category_id #title.strip() # 
            #sites/MLA/domain_discovery/search?limit=1&q=fiat%20uno
    ruta = f'/categories/{user_category_id}'
    print('rutaCategoria: ',ruta)

    secure = 0
    while secure == 0:
        # #try:
        # Request a la api de mercadolibre
        #rta = api_instance2.resource_get(ruta,'') 
        response = apiMeliController('GET',ruta,'','')
        rta = json.loads(response.text)
        status_code = (response.status_code)
        
        if status_code >= 500 or status_code == 429:
            print(f'\nError {status_code}... reintentar request...\n')
            secure = 0 # Reintentar
            continue
        elif status_code >=200 and status_code < 299:
            secure = 1 #todo bien
        else:
            print(f'\nNuevo Error: {status_code}')
            secure = 2 # Pasar al siguiente producto
            continue

        #print(f'rtaType: {type(rta)}')
        # Se almacena la respuesta de mercadolibre en la variable rta
        print('predictorCategorias: ',rta)
        #print(f'title: {title}\n') # producto a predecir categoria
        try:
            #user_category_id = (rta[0])['user_category_id']  # categoria obtenida
            #domain_name = (rta[0])['domain_name']
            #category_name = domain_name + ', ' +(rta[0])['category_name']  # nombre de la categoria
            category_name = rta['name']
        except:
            #user_category_id = meli_site_id + '3530'
            domain_name = 'Otros'
            category_name = domain_name + ' Otros' 
                #print(f'\n {user_category_id} : {category_name} \n') # printeo
                #print(f'\n rta: {rta} \n')  # printeo todo el json de rta
                #print(type(rta[0])) # printeo el tipo de dato
                # secure = 2
            
        # # except Exception as e:
            
        # #     print("Exception Error: -------------------> %s\n" % e.body)
        # #     # Crear code a prueba de errores
        # #     if e.status == 500:
        # #         print('\nError del Servidor 500... reintentar request...\n')
        # #         secure = 0 # Reintentar
        # #     elif e.status == 429:
        # #         print('\nError Too Many Request... reintentar request...\n')
        # #         secure = 0 # Reintentar
        # #     else:
        # #         print('\nNuevo Error')
        # #         secure = 2 # Pasar al siguiente producto


    dict_sku = {} 
    dict_sku["id"] = "SELLER_SKU"
    dict_sku["value_name"] = sku

    body_attr = [dict_sku] 
    # Atributos de la cateogoria, con formato del body json
    # lista de diccionarios
    #attr_dict = {} #diccionario para almacenar datos temporalmente

    ruta = '/categories/'+ user_category_id  + '/attributes'
    # Ruta a la api para obtener atributos de la categoria 

    secure = 0
    while secure == 0:

        # # try:
            # Obtener Atributos - Request API MELI
            #atributos = ((api_instance2.resource_get(ruta,'')))
        response = apiMeliController('GET',ruta,'','')
        atributos = json.loads(response.text)
        status_code = (response.status_code)
        
        if status_code >= 500 or status_code == 429:
            print(f'\nError {status_code}... reintentar request...\n')
            secure = 0 # Reintentar
            continue
        elif status_code >=200 and status_code < 299:
            secure = 1 #todo bien
        else:
            print(f'\nNuevo Error: {status_code}')
            secure = 2 # Pasar al siguiente producto
            continue
            #print(f'pegueleee {atributos}')
            # request a la api de mercadlibre para obtener los atributos
            # secure = 2

        # # except Exception as e:

        # #         print(f"Error: {e.body} ")
        # #         # Crear code a prueba de errores
        # #         if e.status == 500:
        # #             print('\nError del Servidor 500... reintentar request...\n')
        # #             secure = 0 # Reintentar
        # #         elif e.status == 429:
        # #             print('\nError Too Many Request... reintentar request...\n')
        # #             secure = 0 # Reintentar
        # #         else:
        # #             print('\nNuevo Error')
        # #             secure = 2 # Pasar al siguiente producto 

    # Siguiente code: Dise;ado en Google Colab, miangel0.7@gmail.com
    #print('atributos: ',atributos)
    # Laboratorio de atributos Mercadolibre
    for i in range (len(atributos)):

        #units = 0 
        # units, me indica si el atributo tiene unidades.

        # # # # try:
        # # # #     # si existe el tag required es un atributo obligatorio
        # # # #     if atributos[i]['tags']['required']:
        # # # #         # Si existe
        # # # #         # # # # Alamaceno el id del atributo (BRAND,MODEL,ETC)
        # # # #         # # # attr_dict['id'] = atributos[i]['id']
        # # # #         # # # #attr_dict['name'] = atributos[i]['name']
        # # # #         # # # # data_name  = valor a asignar al attr
        # # # #         # # # data_name = atributos[i]['name']
        # # # #         # # # attr_dict['value_name'] = data_name
        # # # #         # # # #test = attr_dict['id']
        # # # #         # # # #print(f'\n{test}: {data_name} \n')
        # # # #         # # # body_attr.append(attr_dict)
        # # # #         # # # attr_dict = {}
        # # # #         body_attr = attrMeliLogic(i,atributos,body_attr,attributesDict,brand,model,weigth)
        # # # #         #print('body_attr: ',body_attr)
                
        # # # # except KeyError:
            
        # Preguntar si el atributo de meli es oculto
        try:
            # Pregunto si el atrributo es oculto    
            if atributos[i]['tags']['hidden'] :
                # Atributo Oculto - No hacer nada
                continue

        except Exception as e: 
            # Pregunto si el atrributo es de solo lectura 
            try:  
                if atributos[i]['tags']['read_only'] :
                    # Atributo Solo Lectura - No hacer nada
                    continue
            except KeyError:
                
                body_attr = attrMeliLogic(i,atributos,body_attr,attributesDict,brand,model,weigth)
                #Atributo no oculto. Puede ser Requerido o no.
                #se llena para subir % calidad de la publicacion


    return user_category_id, category_name, body_attr

            