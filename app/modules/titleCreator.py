# Este modulo crea un titulo para productos con malos titulos

'''
El título es la clave para que los compradores encuentren el producto.
Por eso, debe ser lo más explícito posible.
Genera el título con:
    Producto + Marca + modelo del producto + algunas 
    especificaciones que ayuden a identificar el producto.
'''

def titleCreator(response,attributesTable,brand,categoria,modelo,userTitle):
#title = response.css('span.product-title-word-break::text').get()

    try:
        title = response.css('span#productTitle::text').get()
    except:
        title = '*** captcha ***'   
   
    if userTitle == 'vacio' or userTitle == '' or title == '*** captcha ***':
        title = title
    else:
        title = userTitle
    
    title = title.replace('\n','')
    #print(f'\n\n * * * title_orig: {title}') #testing
    title = title.replace(" - "," ").replace("-"," ").replace(",","").replace("|"," ").replace("(","").replace(")","").replace("@"," ").replace("Amazon","").replace('amazon','')
    #print(f'title: {title}, type: {type(title)}')  #pruebas
    #print(f'title original: {title}')
    return title   
    # # # if (brand == 'null' or modelo == 'null' or categoria == 'null'):
    # # #     #USAR TITULO EXTRAIDO
    # # #     pass
    
    # # # else:

    # # #     try:
    # # #         #Eliminar el plural a la categoria
    # # #         categoria = categoria.split(" ")
    # # #         print(categoria)
    # # #         if categoria[0] == "":
    # # #             print('entro aqui')
    # # #             categoria.pop(0)
    # # #         categoria = ' '.join(str(item) for item in categoria)
    # # #         print(categoria)

    # # #         categoriaSplit = categoria.split(" ")
    # # #         longCategoria = len(categoriaSplit)
    # # #         print(categoriaSplit)

    # # #         primeraPalabra = list(categoriaSplit[0])
    # # #         print(primeraPalabra)

    # # #         longPrimeraPalabra = len(primeraPalabra)

    # # #         if primeraPalabra[longPrimeraPalabra-2] == 'e' and primeraPalabra[longPrimeraPalabra-1] == 's':
    # # #             print('termina en es')
    # # #             primeraPalabra.pop()
    # # #             primeraPalabra.pop()
    # # #             primeraPalabraString = ''.join(str(item) for item in primeraPalabra)
    # # #             print(primeraPalabraString)

    # # #         elif primeraPalabra[longPrimeraPalabra-1] == 's':
    # # #             print('termina en s')
    # # #             primeraPalabra.pop()
    # # #             primeraPalabraString = ''.join(str(item) for item in primeraPalabra)
    # # #             print(primeraPalabraString)
    # # #         try:
    # # #             categoriaSplit[0] = primeraPalabraString
    # # #             categoriaCorregida = ' '.join(str(item) for item in categoriaSplit)
    # # #             print(categoriaCorregida)
    # # #         except:
    # # #             categoriaCorregida = categoria
    # # #             print(categoriaCorregida)
            
    # # #         values = []
    # # #         #subatributo = {}
    # # #         # Atributos - volvemos lista
    # # #         attributesTable =  attributesTable.split("/@")
    # # #         for attr in attributesTable:
    # # #             aux = attr.split(":")
    # # #             #subatributo[str(aux[0])] = aux[1]
    # # #             values.append(aux[1])

    # # #         #print(subatributo)
    # # #         # Armar titulo
    # # #         title = categoriaCorregida + ' ' + brand + ' ' + modelo + ' '
    # # #         title = title.replace('\n','').replace(" - "," ").replace("-"," ").replace(",","").replace("|"," ").replace("(","").replace(")","").replace("@"," ").replace(".","").replace("  "," ")
    # # #         print(f' \n\n NUEVO TITLEEEE ANTES DE ATTR:{title}\n\n')
    # # #         longitudTitle1 = len(title)
    # # #         numeroCaracteresDisponibles = 60 - longitudTitle1
    # # #         contador = 0
    # # #         for value in values:
    # # #             if (len(value)  < numeroCaracteresDisponibles/2 and contador < 2 and value != (" "+brand) and value != (" "+modelo)):
    # # #                 title = title + value + ' '
    # # #                 contador = contador + 1  
    # # #         print(f' \n\n\nNDSFJDFJSBDF: {title}')

    # # #     except:
    # # #         pass

    