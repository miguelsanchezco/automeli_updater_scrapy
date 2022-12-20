# Selectores 2, for scrape data uses
# Creado 20/06/2021
# Actualizacion: 13/08/2021
# Miguel Sanchez Ramirez
# Se crean varias opciones de selectores por cada atributo a extraer 


def selectores_css2(response):
# Funcion principal

    #CATEGORIAS <<< <<< <<<
    
    selectores = ['ul.a-size-small a::text', 'a.a-color-tertiary::text'] 
    amzn_category = ''

    for selector in selectores:
        try:
            categorias = response.css(selector).getall()
            #print(f'listaCategorias {categorias}')
            if categorias:
                # for categoria in categorias:
                #     amzn_category = amzn_category + '@' + categoria
                # break
                amzn_category = categorias.pop()
        except:
            print('error selector categoria.')
            continue
    


    # # # try:

    # # #     categorias = response.css('ul.a-size-small a::text').getall()
    # # #     #selector css de categoria
    # # #     print(categorias)
    # # #     if categorias:
    # # #         categoria = categorias.pop()
    # # #         #si se obtuvo resultados hacer!
    # # #         #longitud = len(categorias)
    # # #         #for i in range(longitud-1):
    # # #         #    categorias.pop(i) 
    # # #         #    print(categorias)
    # # #         #categorias.pop(0) 
    # # #         #eLimino la categoria principal, dejo las subcategorias unicamente
    # # #         print('\n1. Selector Categoria\n')
    # # #         #convertir lista de categorias en cadena de texto
    # # #         #for categ in categorias:
    # # #         #    categoria = str(categoria + '@' + categ)
    # # #             #entre subcategoria y subcategoria pongo un @
    # # #     else:
    # # #         #En caso de que el primer selector falle, hacer!
    # # #         categorias = response.css('a.a-color-tertiary::text').getall()   
    # # #         print(categorias)
    # # #         if categorias:
    # # #             categoria = categorias.pop()
    # # #             #si se obtuvo resultados hacer!
    # # #             # longitud = len(categorias)
    # # #             # for i in range(longitud-1):
    # # #             #     categorias.pop(i) 
    # # #             #     print(categorias)
    # # #             #categorias.pop(0) 
    # # #             #ELimino la categoria principal, dejo las subcategorias
    # # #             print('\n2. Selector Categoria\n')
    # # #             #convertir lista en string
    # # #             #for categ in categorias:
    # # #             #    categoria = str(categoria + '@' +categ)
    # # #                 #entre subcategoria y subcategoria pongo un @
    # # #         else:
    # # #             print('No Sirve selector css de categorias.!')
    # # #             categoria = 'null'
  
    # # # except:
    # # #     categoria = 'null'
    # # #     print('Error, Item No Categorizado.')


    amzn_category = amzn_category.replace('\n', '').replace('  ','').replace('  ', ' ').replace('@',' ').strip()
    #eliminamos los saltos de linea, los espacios en blanco. No modificar esta parte. ya funciona!
    
    # # # # try:
    # # # #     categoria = categoria.split(" ")
    # # # #     print(categoria)
    # # # #     if categoria[0] == "":
    # # # #         categoria.pop(0)
    # # # #     categoria = ' '.join(str(item) for item in categoria)
    # # # # except:
    # # # #     pass
    
    print(f'Amzn Categoria: {amzn_category}\n')
    #CATEGORIAS <<< <<< <<<

    #tr.a-spacing-none:nth-child(1) > td:nth-child(2) > span:nth-child(1)
    #MARCA <<< <<< <<<
    brand = ''
    selectoresBrand = [ 
        "tr.po-brand td:nth-child(2) span::text", #td:nth-child(2)::text
        "tr:contains('Brand') td::text",
        "tr:contains('Fabricante') td::text",
        "tr:contains('Marca') td::text",
        "tr:contains('Marca') td span.a-size-base::text"
    ]

    for index,selector in enumerate(selectoresBrand):
        if index == len(selectoresBrand)-1: #ultimo selector
            brand = response.css(selector).get()
            if brand:
                brand = brand.strip()
                if brand != '':
                    print(f'marca{index}: {brand}')
                    break
        else:
            try:
                #uso un try porque esto tratando de ingresar a un indice de una lista que puede no existir
                brand = response.css(selector).getall()[1]
                brand = brand.strip()
                # Tomo el segundo valor, Marca:MALOSOPT, porque el primer valor es la palabra 'Marca'.
                print(f'marca{index}: {brand}')
                break
            except:
                print('No hay info de la Marca/Fabricante o no Selector css.')  
                continue

    # # # brand = 'null'
    # # # brand = response.css("tr:contains('Brand') td::text").get()
    # # # if brand:
    # # #     print(f'marca1: {brand}')
    # # # else:
    # # #     try:
    # # #         #uso un try porque esto tratando de ingresar a un indice de una lista que puede no existir
    # # #         brand = response.css("tr:contains('Marca') td span.a-size-base::text").getall()[1]
    # # #         # Tomo el segundo valor, Marca:MALOSOPT, porque el primer valor es la palabra 'Marca'.
    # # #     except:
    # # #         pass
    # # #     if brand:
    # # #         print(f'marca2: {brand}')
    # # #     else:
    # # #         brand = response.css("tr:contains('Fabricante') td::text").get()
    # # #         if brand:
    # # #             print(f'marca3: {brand}')
    # # #         else:
    # # #             brand = response.css("tr:contains('Marca') td::text").get()
    # # #             if brand:
    # # #                 print(f'marca4: {brand}')
    # # #             else:
    # # #                 print('No hay info de la Marca/Fabricante o no Selector css.')    
    
    
    if (brand == None or brand == '' or brand == ' '):
        brand = 'Genérica'
    else:
        brand = brand.replace('\n','').replace('\u200e','').strip()
    
    #print(f'marca: {brand}')

    #MARCA <<< <<< <<<

    modelo = 'null'
    selectoresModelo = [ "tr:contains('Número de modelo') td::text",
                         "tr:contains('Model number') td::text",
                         "tr:contains('Número de parte') td::text",
                         "tr:contains('Número de modelo del producto') td::text"
                    ]
    for index,selector in enumerate(selectoresModelo):
        modelo = response.css(selector).get()
        if modelo:
            print(f'modelo{index}: {modelo.strip()}')
            break

    # # # # #MODELOO <<< <<< <<<
    # # # # modelo = 'null'
    # # # # modelo = response.css("tr:contains('Número de modelo del producto') td::text").get()
    # # # # if modelo:
    # # # #     print(f'modelo1: {modelo.strip()}')
    # # # # else:
    # # # #     modelo = response.css("tr:contains('Número de modelo') td::text").get()
    # # # #     if modelo:
    # # # #         print(f'modelo2: {modelo.strip()}')
    # # # #     else:
    # # # #         modelo = response.css("tr:contains('Model number') td::text").get()
    # # # #         if modelo:
    # # # #             print(f'modelo3: {modelo.strip()}')
    # # # #         else:
    # # # #             modelo = response.css("tr:contains('Número de parte') td::text").get()
    # # # #             if modelo:
    # # # #                 print(f'modelo4: {modelo.strip()}')
    # # # #             else:
    # # # #                 print('No hay info del Modelo o no Selector css')
    

    if modelo == None or modelo == '' or modelo == ' ':
        modelo = 'Model'
    else:
        modelo = modelo.replace('\n','').replace('\u200e','').strip()

    print(f'modelo definitivo: {modelo}')

    #MODELOO <<< <<< <<<


    #N Reviesws
    nReviews = 'null'
    # # # nReviews = response.css('#averageCustomerReviews_feature_div span.a-size-base::text').get()
    # # # if nReviews:
    # # #     print(f'nReviews: {nReviews}')
    
    # # # if nReviews == None or nReviews == '' or nReviews == ' ':
    # # #     nReviews = response.css('span#acrCustomerReviewText::text').get()
    # # #     if nReviews == None or nReviews == '' or nReviews == ' ':
    # # #         nReviews = 'null'
    # # # else:
    # # #     nReviews = nReviews.replace('\n','').replace('\u200e','')
    # # #     nReviews = nReviews.split(" ")[0]


    #Puntuacion
    score = 'null'
    # # # score = response.css('span[data-hook="rating-out-of-text"]::text').get()
    # # # if score:
    # # #     print(f'score: {score}')
    
    # # # if score == None or score == '' or score == ' ':
    # # #     score = 'null'
    # # # else:
    # # #     score = score.replace('\n','').replace('\u200e','')
    # # #     score = score.split(" ")[0]
    

    # # # #PRODUCTO EN AMAZON DESDE...
    # # # antiguedad = 'null'
    # # # antiguedad = response.css("tr:contains('Producto en amazon.com desde') td::text").get()
    # # # if antiguedad:
    # # #     print(f'antiguedad: {antiguedad}')
    
    # # # if antiguedad == None or antiguedad == '' or antiguedad == ' ':
    # # #     antiguedad = 'null'
    # # # else:
    # # #     antiguedad = antiguedad.replace('\n','').replace('\u200e','')



    return amzn_category, brand, modelo, nReviews, score #, antiguedad



#CATEGORIAS
#response.css('ul.a-size-small a::text').getall()
#response.css('a.a-color-tertiary::text').getall()


#VENDIDO Y ENVIADO POR

# Con esta selecciono enviado y vendido por Amazon.com  o enviado por un vendedor
#response.css('span.tabular-buybox-text::text').getall()

# Con esta selecciono vendido por un vendedor cuando no es amazon.
#response.css('span.tabular-buybox-text a::text').getall()

# null cuando scrapea desde otro pais diferente a USA o el articulo no esta disponible o tiene variantes.


# NUEVO o usadoo o refurbished-renovado
#response.css('div.olp-text-box span::text').getall()


# REFURBISHEEDD si existe entonces es refurbished
#response.css('div#certifiedRefurbishedVersion_feature_div')  #retorna lista, si no hay nada retorna lista vacia
#response.css('div#certifiedRefurbishedVersion_feature_div').get()  # retorna string, si no hay nada no retorna nada
#response.css('div#renewedProgramDescriptionAtf_feature_div').get()  # retorna string, si no hay nada no retorna nada



#PESO DEL PRODUCTO
#response.css("tr:contains('Peso del producto') td::text").get()
#response.css("tr:contains('Item Weight') td::text").get()
#response.css("tr:contains('Item weight') td::text").get()


#VOLUMEN
#response.css("tr:contains('Dimensiones del producto') td::text").get()
#response.css("tr:contains('Dimensiones del paquete') td::text").get()
#response.css("tr:contains('Package Dimensions') td::text").get()
#response.css("tr:contains('Package dimensions') td::text").get()
#response.css("tr:contains('Product Dimensions') td::text").get()
#response.css("tr:contains('Product dimensions') td::text").get()



#MARCA
#response.css("tr:contains('Brand') td::text").get()
#response.css("tr:contains('Marca') td::text").get()
#response.css("tr:contains('Fabricante') td::text").get()


#MODELOO
#response.css("tr:contains('Número de modelo del producto') td::text").get()
#response.css("tr:contains('Número de modelo') td::text").get()
#response.css("tr:contains('Model number') td::text").get()
#response.css("tr:contains('Número de parte') td::text").get()


#N Reviesws
#response.css('#averageCustomerReviews_feature_div span.a-size-base::text').get()
#Puntuacion
#response.css('span[data-hook="rating-out-of-text"]::text').get()


#PRODUCTO EN AMAZON DESDE...
#response.css("tr:contains('Producto en amazon.com desde') td::text").get()