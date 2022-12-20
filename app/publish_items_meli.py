
""" 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Para ejecutar este archivo tener en cuenta que debe pasar el número del ACCOUNT
como parámetro de entrada en el comando de ejecución. Ejemplo:
python3 file_name.py 2
donde 2 es el número del ACCOUNT que se usará.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""


#import meli
from tabulate import tabulate
from modules.api_bodys import body_generator
from modules.api_publisher import publisher
#from modules.mysqlCRUD import DataLogManager
from modules.cronometro import access_token_memory
from modules.api_description import description_creator



def imagesToMeli(images):
  """
  Takes a string of urls of images separated by | and returns a list of dictionaries with each url

  input:
    images: (str) cointains the urls separated by |

  output:
    (list of dicts) with the key: source and the value: image url
  """
  images_list = images.split("|")
  return [{"source": image} for image in images_list]


def text_shortener(text, characters):
    # Programa acortador de titulos a una cantidad de caracteres, characters
    
    len_title = len(text)  
    if len_title <= characters:
        pass
    # print('text OK 1')
    # print('text definitivo: ', text)
    # print('len_title: ', len(text))
    elif text[characters:][0] == " " or text[:characters][-1] == " " :
        text = text[:characters]
    # print('text OK 2')
    # print('text definitivo: ', text)
    # print('len_title: ', len(text))
    else:
        for i in reversed(range(characters)):
            cutting_title = text[:characters][i]
            if cutting_title == " ":
                text = text[:i]
                # print('text definitivo: ', text)
                # print('len_title: ', len(text))
                break   
    return text


def create_table(attributes_dict):
    """
    Takes a string that contains a table html code with info about the attributes and converts it
    into a table using module tabulate

    input:
    attributes_html: (str) contains the html code for the attributes table

    output:
        table: (str) the formatted table
    """
    # dfs = pd.read_html(attributes_html)
    # df = dfs[0]  # pd.read_html reads in all tables and returns a list of DataFrames
    keys = attributes_dict.keys()
    values = attributes_dict.values()
    new_dict = {"Caracteristica": keys, "Valor": values}
    table = tabulate(new_dict, tablefmt="plain")
    return table


def publishInMeli(data_to_yield,seller_id,databaseName,dataUser,listing_type_id,access_token,testMode):

        meli_currency = dataUser.loc[0,'meli_currency']
        #api_client = meli.ApiClient()
        #api_instance2 = meli.RestClientApi(api_client)
        #access_token = access_token_memory(seller_id,databaseName)  #cronometro modulo
        #print('Estoy aqui')
        
        # # meli_price = data_to_yield['meli_price']
        
        # Definiendo el tiempo de la garantia.
        # # if meli_price < 200000:
        # #     WARRANTY_TIME = "1 mes"
        # # elif meli_price >= 200000 and meli_price < 400000: 
        # #     WARRANTY_TIME = "3 meses"
        # # elif meli_price >= 400000:
        # #     WARRANTY_TIME = "6 meses"

        if data_to_yield['description_1'] == 'null':
            if data_to_yield['description_2'] == 'null':
                description_final = ''
            else:
                description_final = '\n' + text_shortener(data_to_yield['description_2'],1000) + '\n'
        else:
            description_final = '\n' +  text_shortener(data_to_yield['description_1'],1000) + '\n'
        # # Publicador de Productos
        # publisher(body,sku,description,access_token,ACCOUNT) #descripcion es una lista
        sku = data_to_yield['sku']
        title60 = text_shortener(data_to_yield['title'],60)
        
        images_from_df = data_to_yield["images_concat"] 
        images_logo = dataUser.loc[0,'logos_concat']
        if images_logo != '':
            images_from_df = images_from_df + "|" + images_logo
        imagenes =  imagesToMeli(images_from_df)

        print('title60:',title60)
        #print('imagenes: ',imagenes)

        # Obtenemos el body para publicar
        body = body_generator(data_to_yield,title60,imagenes,dataUser,listing_type_id) 
        
        print(f'\nBODY: {body}\n')

        caracteristicas = create_table(data_to_yield['amzn_attributes']) if data_to_yield['amzn_attributes'] != {} else ''
        # print('voy aqui 1')
        # print(caracteristicas)
        description = description_creator(data_to_yield['title'],title60,caracteristicas,description_final,dataUser)
        #print(description)
        # # # # # Publicador de Productos
        # print('voy aqui 2')
        publisher(body,sku,description,access_token,seller_id,data_to_yield,meli_currency,databaseName,testMode) #descripcion es una lista
