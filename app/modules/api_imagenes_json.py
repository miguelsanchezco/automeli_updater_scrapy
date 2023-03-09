# Last-updated 22/11/2021
# Modulo Imagenes
# Este modulo se encarga de arreglar el json que se enviara
# a traves de la API para publicar las imagenes de cada producto o item
# Este modulo tendra una unica funcion
# Este modulo es generico y se puede usar para publicar cualquier item
# -------------------------------------------------------------------

import os
import re

#from cv2 import data
# Expresiones regulares

path = '/tmp/' 

# depura las imagenes scrapeadas por amazon
def img_depuration(data_to_yield, response):  #data_to_yield,response

    #data_to_yield = {}
    # I M A G E N E S .....................................................
    #(?<="hiRes":")(.*?)(?=")
    #imgs = re.findall('(?<="hiRes":")(.*?)(?=")',response.text) #FUncional


    maxImgQuantity = 7
    # EL numero 7 es porque asi lo defini, como la cantidad max de imagenes a extraer.

    #OBTENGO LA CANTIDAD DE IMAGENES QUE TIENE EL PRODUCTO
    imgQuantity = len(response.css('div#altImages li.a-spacing-small.item').getall())


    print(f'imgQuantity: {imgQuantity} !!!')
    # # if imgQuantity == 0:
    # #     #OBTENGO LA CANTIDAD DE IMAGENES QUE TIENE EL PRODUCTO SELECTOR 2
    # #     ##altImages > ul > li:nth-child(4)
    # #     imgQuantity = len(response.css('div#altImages li.a-spacing-small.item').getall())

    if imgQuantity > maxImgQuantity : 
        imgQuantity = maxImgQuantity
    elif imgQuantity == 0:
        imgQuantity = 4
    
    #VERIFICAMOS LA EXISTENCIA DE VIDEO
    #Este selector captura las imagenes
    IMGS = response.css('div#altImages li.a-spacing-small.item span img::attr(src)').getall()
    print(f'IMGS: {IMGS}')
    if imgQuantity >= 1 and len(IMGS)>=1:
        # # # match1 = re.search('play-button',IMGS[-1]) 
        # # # match2 = re.search('play-icon',IMGS[-1]) 
        # # # #buscamos la palabra play-button en la url de la ultima imagen
        # # # if match1 or match2: 
        # # #     #si se encuentra video, se disminuye en 1 imgQuantity
        # # #     imgQuantity = imgQuantity - 1
        # # #     if imgQuantity >=2 and len(IMGS)>=2:
        # # #         match1 = re.search('play-button',IMGS[-2])
        # # #         match2 = re.search('play-icon',IMGS[-2]) 
        # # #         #buscamos la palabra play-button en la penultima imagen
        # # #         if match1 or match2: 
        # # #             imgQuantity = imgQuantity - 1 
        # # #             #si se encuentra video, se disminuye en 2 la cantidad de imagenes
        for image in IMGS:
            if 'play-button' in image or 'play-icon' in image:
                imgQuantity = imgQuantity - 1 
                
    print(f'imgQuantityCorregido: {imgQuantity} !!!')
    #Inicializo las imagenes para yield
    for i in range(maxImgQuantity):
        indice = 'img' + str(i) 
        data_to_yield[indice] = 'null'
    
    list_images = ['null']*maxImgQuantity # Lista de imagenes extraidas
    #list_images = [] <<<<<<<<<<

    # Esta expresion regular halla todas las imgs HD sin que se repitan
    #(?<="hiRes":"https:\/\/images-na\.ssl-images-amazon\.com\/images\/I\/)(.*?)(?=\.) #vieja expresion r
    #(?<="hiRes":"https:\/\/m\.media-amazon\.com\/images\/I\/)(.*?)(?=\.)
    #m.media-amazon.com
    selectorlarge = '(?<="large":)(.*?)(?=,)'
    # print('...large...')
    imgslarge = re.findall(selectorlarge,response.text)
    # for large in imgslarge:
    #     print(large)
    #     print('_____')
    selectorhiRes = '(?<="hiRes":)(.*?)(?=,)'
                    # [ '(?<="hiRes":"https:\/\/m\.media-amazon\.com\/images\/W\/)(.*?)(?=\.)',
                    #   '(?<="hiRes":"https:\/\/m\.media-amazon\.com\/images\/I\/)(.*?)(?=\.)',
                    #   '(?<="hiRes":"https:\/\/images-na\.ssl-images-amazon\.com\/images\/I\/)(.*?)(?=\.)',
                    #   '(?<="hiRes":"https:\/\/images-na\.ssl-images-amazon\.com\/images\/W\/)(.*?)(?=\.)', 
                    #  ]
    # contador = 0
    # winner = ''
    # for selector in listSelectores:
    #     imgs = re.findall(selector,response.text)
    #     print(f'selector : {selector} ',)
    #     if imgs == []:
    #         continue
    #     else:
    #         print(f'imgs despues de re.findall : {len(imgs)}')
    #         if contador == 0:
    #             winner = selector
    #             imgsCountAnterior = len(imgs)
    #         else:
    #             if len(imgs)>imgsCountAnterior:
    #                 winner = selector
    #                 imgsCountAnterior = len(imgs)
    #             else:
    #                 continue
    #         contador = contador +1
    # #print(f'winnerSector: {winner}')
    # if winner != '':
    imgshiRes = re.findall(selectorhiRes,response.text)
    # print(f'imgs using winnerSector: {imgs}')
    print('...hiRes...')
    for index,hires in enumerate(imgshiRes[:7]):
        print(hires)
        if "null" in hires:
            imgshiRes[index] = imgslarge[index]
        print('_____')
        imgshiRes[index] = imgshiRes[index].split('.')[-3].split('/')[-1]

    imgs = imgshiRes
    print(f'imgsCorregidas: {imgs[:7]}')
    # # # imgs = re.findall('(?<="hiRes":"https:\/\/m\.media-amazon\.com\/images\/I\/)(.*?)(?=\.)',response.text)
    # # # #print(imgs)
    # # # if imgs == []:
    # # #     imgs = re.findall('(?<="hiRes":"https:\/\/images-na\.ssl-images-amazon\.com\/images\/I\/)(.*?)(?=\.)',response.text)
    # # #     #print('HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA HIRESSSSSSSSSSSSSSSSSSSS')
        #file = open(path + 'responseimgs.txt', "w")
        #file. write(response.text + os.linesep)
        #re.findall('"hiRes":"',response.text)
    #imgs almacena los identificadores unicos de cada imagen, ejemplos 5f85fds78fd5
    #raiz_url_img = 'https://images-na.ssl-images-amazon.com/images/I/'  #anterior raiz
    raiz_url_img = 'https://m.media-amazon.com/images/I/'  #nueva raiz
    # raiz de las imagenes
    
    # # # if imgs:
    # # #     #ELimino duplicados
    # # #     imgs = list(set(imgs))

    if len(imgs)>=maxImgQuantity:
        # Hacer un bucle de 0 a 6
        # guardar las 7 primeras imagenes
       
        for i in range(imgQuantity):  # Solo deseo las imagenes del producto
            
            if len(imgs[i]) > 16:
                imgs[i] = imgs[i].split('/images/I/')[1]  #IMAGERENDERING_521856-T2/images/I/31yhyYh4RLS

            indice = 'img' + str(i) #img0, img1, img2...
           
            data_to_yield[indice] = raiz_url_img + imgs[i] + '.jpg' #concatena url_raiz + id_imagen + extension .jpg

            list_images[i] = (raiz_url_img + imgs[i] + '.jpg')  #almaceno en list imagenes   
            #list_images.append(raiz_url_img + imgs[i] + '.jpg')  #almaceno en list imagenes


    elif len(imgs)>0:
        # Hay entre 1 y 6 imagenes
        
        #print(f'# de imagenes: {len(imgs)}')
        for i in range(len(imgs)):

            if len(imgs[i]) > 16:
                imgs[i] = imgs[i].split('/images/I/')[1]  #IMAGERENDERING_521856-T2/images/I/31yhyYh4RLS

            indice = 'img' + str(i) #img0, img1, img2...

            data_to_yield[indice] = raiz_url_img + imgs[i] + '.jpg'   
            #concatena url_raiz + id_imagen + extension .jpg

            list_images[i] = (raiz_url_img + imgs[i] + '.jpg')
            #list_images.append(raiz_url_img + imgs[i] + '.jpg')  
    

    else:
        # No hay imagenes HD
        # Obtenemos imagenes de mas baja resolucion
        print('NO HAY IMAGENES FULL HD')

        #imgs = re.findall('(?<="main":")(.*?)(?=")',response.text)
        #imgs = re.findall('"main":{"(.*?)"',response.text)
        # "large":"https://images-na.ssl-images-amazon.com/images/I/
        #"https:\/\/m\.media-amazon\.com\/images\/I\/)
        #(?<="large":"https:\/\/images-na\.ssl-images-amazon\.com\/images\/I\/)(.*?)(?=\.)  #anterior exp regular
        imgs = re.findall('(?<="large":"https:\/\/m\.media-amazon\.com\/images\/I\/)(.*?)(?=\.)',response.text)
        #print(imgs)
        if imgs == []:
            imgs = re.findall('(?<="large":"https:\/\/images-na\.ssl-images-amazon\.com\/images\/I\/)(.*?)(?=\.)',response.text)
            #print('HOOOOOOOOOLAAAAAAAAAAAAAAAAAAAAAAAA LAAAAAAAARRRRRRRRRGEEEEEEEEEEEEEEEEEEEEE')
            #re.findall('"large":"',response.text)
        #print(f'imagenes Large: {imgs}')
        
        # # # if imgs:
        # # # #ELimino duplicados
        # # #     imgs = list(set(imgs))

        if len(imgs)>=maxImgQuantity:
        
            for i in range(imgQuantity):  #
                indice = 'img' + str(i)
                data_to_yield[indice] = raiz_url_img + imgs[i] + '.jpg'  
                # data_to_yield[img0] = 'https:..' 
                list_images[i] = (raiz_url_img + imgs[i] + '.jpg') 
                #list_images.append(raiz_url_img + imgs[i] + '.jpg') 
                # list imagenes        
                #print(data_to_yield)

        elif len(imgs)>0:
            # Hay entre 1 y 6 imagenes
            #print('Hay menos de 7 imagenes')
            print(f'# de imagenes: {len(imgs)}')
            for i in range(len(imgs)):
                indice = 'img' + str(i)
                data_to_yield[indice] = raiz_url_img + imgs[i] + '.jpg' 
                # data_to_yield[img0] = 'https:..'  
                list_images[i] = (raiz_url_img + imgs[i] + '.jpg')
                #list_images.append(raiz_url_img + imgs[i] + '.jpg') 
                # list imagenes         
            #print('sku + imagenes ',data_to_yield)

        else:
            print("No images in this product.")
            # Nada que hacer

    concatenacion = ''
    for i in range(imgQuantity):
        if list_images[i] != 'null':
            concatenacion += list_images[i] +' '
    images_in_list = concatenacion.split()           
    data_to_yield['images_concat'] = '|'.join(images_in_list)
    return data_to_yield, list_images #data_to_yield, list_images

    '''
        Actualizacion 22/11/2021
        Se agreg[o] funcionalidad para seleccionar solo las imgs del producto,
        antes se estaban enviando imgs que no correspondian al producto,
        esto debido a las variantes que tenia.  
    '''
    
    ##COMENTE TOD0 EL CODIGO A ACONTINUACION PARA REALIZAR UNICAMENTE EXTRACCION DE DATOS
    ##SE DEJA EL PROCESAMIENTO PARA DESPUES.
    # # # # I M A G E N E S .....................................................
    
    # # # imagenes = [] # List donde se almacenan los dict's
    # # # img_dict = {} # Diccionario, clave - valor para almacenar cada img 

    # # # for image in list_images:
    # # #     img_dict['source'] = image   # Diccionario 'source':'https://data.com/images.png'
    # # #     imagenes.append(img_dict)    # Lista , append , guardo el diccionario
    # # #     img_dict = {}                # Limpio el Diccionario
    # # #     #print(imagenes)             # Para test 

    # # # # Logos de Just Market Colombia  -------------------------------------------
    # # # logos = ['https://i.postimg.cc/ZTXJ2Dxy/SOMOS-IMPORTADORES.png',
    # # #          'https://i.postimg.cc/wqJ9pcw4/SOMOS-IMPORTADORES-2.png']
    # # #          #'https://http2.mlstatic.com/D_NQ_NP_2X_923312-MCO44322378549_122020-F.webp'] 
    # # #          #Logo de JW, Logo de Envio Gratis y Vacio. Creados By: Nati
    
    # # # n_logos = len(logos)  # numero de imagenes aux

    # # # for i in range(n_logos): 
    # # #     img_dict['source'] = logos[i]
    # # #     imagenes.append(img_dict)
    # # #     img_dict = {}
    # # #     #print(imagenes)
    
    # # # #print(f'Imagenes json: {imagenes}')

    # # # return data_to_yield, imagenes
    # # # # Retornamos una lista de diccionarios



# Codigo antiguo, cuando se realizaba publicacion manual.

# # Funcion Unica, recibe dos df: data y data_booleana
# def img(list_images):
#     # Buscamos en el DataFrame en que columna empiezan las imagenes
#     # Para que el bucle for de la funcion imagenes, inicie en el indice 
#     # indicado. 
#     #df_columnas = list(data.index)      # Obtenemos los encabezados del DataFrame
#     #print(df_columnas)                 # Para test
#     #print(data_booleano)               # Para test
#     #bandera = 0                         # variable que almacena el punto de partida de las imagenes
    
#     #for columna in df_columnas:         # Recorremos cada encabezado de las columnas
#     #    if columna == 'img': #or 'img0' # cuando encontremos el encabezado img
#     #        break                       # ROMPEMOS - Se guarda el valor de bandera
#     #    bandera = bandera + 1
    
#     #print(f'Las imagenes en la data inician en el indice {bandera}')
    
#     imagenes = [] # List donde se almacenan los dict's
#     img_dict = {} # Diccionario, clave - valor para almacenar cada img 
#     #counter = 0 # Para test
#     # for i in range(7): # 7 imagenes --------------- Este puede generar errores si en el excel
#     #                    # se cargan mas de 7 imagenes.
#     #                    # Falta agregar 2 o 3 imagenes de La marca! Just Market CO
#     #     #counter = counter +1  # Para test
#     #     #print(f'counter: {counter}') # Para test
#     #     #print(data_booleano[bandera+i]) # Para test
#     #     # el siguiente if arranca en la primera img i=0
#     #     if data_booleano[bandera+i] == False:    # si el valor de la casilla no es nulo,guarde la imagen.
#     #         img_dict['source'] = data[bandera+i] # Diccionario 'source':'https://data.com/images.png'
#     #         imagenes.append(img_dict)            # Lista , append , guardo el diccionario
#     #         img_dict = {}                        # Limpio el Diccionario
#     #         #print(imagenes)                     # Para test 
#     #     #else:
#     #         #break                                # Romper el bucle en caso de que sea True
    
#     for image in list_images:
#         img_dict['source'] = image   # Diccionario 'source':'https://data.com/images.png'
#         imagenes.append(img_dict)            # Lista , append , guardo el diccionario
#         img_dict = {}                        # Limpio el Diccionario
#         ##print(imagenes)                    # Para test 


#     # Logos de Just Market Colombia  -------------------------------------------
#     logos = ['https://http2.mlstatic.com/D_NQ_NP_2X_968308-MCO45604638126_042021-F.webp',
#              'https://http2.mlstatic.com/D_NQ_NP_2X_682797-MCO45604592915_042021-F.webp',
#              'https://http2.mlstatic.com/D_NQ_NP_2X_923312-MCO44322378549_122020-F.webp'] 
#              #Logo de JW, Logo de Envio Gratis y Vacio.

#     for i in range(3): 
#         img_dict['source'] = logos[i]
#         imagenes.append(img_dict)
#         img_dict = {}
#         #print(imagenes)
    
#     return imagenes
#     # Retornamos una lista de diccionarios 
#     # F I N - I M A G E N E S
    
#     # NOTAS ULTIMA VERSION
#     # Hoy 23/04/2021 revise el codigo
#     # Codigo revisado 23/04/2021 ok!

#     # Propuesta de mejora.
#     # Los logos de Just Market son fijos
#     # Podria crearse el json de manera estatica
#     # sin necesidad de que se cree cada vez que 
#     # se ejecute el modulo imagenes. 