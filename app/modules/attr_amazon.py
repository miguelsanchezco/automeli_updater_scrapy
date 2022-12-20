# nymeliapp v 2021.08.14
# Script - Modulo que procesa los atributos scrapeador
# de amazon. para cada item.
# los deja listicos para enviarlos a la descripcion.
# Miguel Sanchez R.   
# Ultima Actualizacion 14/08/2021
# Nota: Esta ready. Gracias a Dios!!!

import re
def attr_amazon(response):

    #print('\nAtributos amazon scrapeados\n')

    nombres_atributos_amazon = ['']
    selectoresNameAttr = [
        'table.a-keyvalue th::text',
        'table#technicalSpecifications_section_1 th::text'
    ]
    for index,selector in enumerate(selectoresNameAttr):
        try:
            nombres_atributos_amazon = response.css(selector).getall()
            if nombres_atributos_amazon != ['']:
                break
        except:
            continue

    nombres_attr_with_links = ['']    
    selectoresNameAttrLinks = [
        'table.a-keyvalue th span[style="white-space: normal"]::text ',
        'table#technicalSpecifications_section_1 th span[style="white-space: normal"]::text '
    ]
    for index,selector in enumerate(selectoresNameAttrLinks):
        try:
            nombres_attr_with_links = response.css(selector).getall()
            if nombres_attr_with_links != ['']:
                break
        except:
            continue    

    #print(f'nombres atributos amazon: {nombres_atributos_amazon}')
    #print(f'nombres atributos con links: {nombres_attr_with_links}')
    
    try:
        # # # # nombres_atributos_amazon = response.css('table.a-keyvalue th::text').getall()
        # # # # if nombres_atributos_amazon:
            
        # # # #     pass
        # # # # else:
        # # # #     nombres_atributos_amazon = response.css('table#technicalSpecifications_section_1 th::text').getall()#technicalSpecifications
        # # # #     if nombres_atributos_amazon:
        # # # #         pass
        # # # #     else:
        # # # #         nombres_atributos_amazon = ['']
        # # # # print(f'nombres atributos amazon: {nombres_atributos_amazon}')
        # # # # nombres_attr_with_links = ['']
        # # # # nombres_attr_with_links = response.css('table.a-keyvalue th span[style="white-space: normal"]::text ').getall()
        # # # # if nombres_attr_with_links:
            
        # # # #     pass
        # # # # else:
        # # # #     nombres_attr_with_links = response.css('table#technicalSpecifications_section_1 th span[style="white-space: normal"]::text ').getall()
            
        # # # #     if nombres_attr_with_links:
        # # # #         pass
        # # # #     else:
        # # # #         nombres_attr_with_links = ['']
        # # # # print(f'nombres atributos con links: {nombres_attr_with_links}')
        
        # # # value_amzn_attribute = ['null']
        # # # value_amzn_attribute = response.css('table.a-keyvalue td::text').getall()
        # # # if value_amzn_attribute:
        # # #     #print(f'valores de los atributos amazon: {value_amzn_attribute}')
        # # #     pass
        # # # else:
        # # #     value_amzn_attribute = ['null']



        # ELiminamos los saltos de linea
        for i in range(len(nombres_atributos_amazon)): 

            nombres_atributos_amazon[i] = nombres_atributos_amazon[i].replace('\n','').replace('\t', '').strip()
                    

        # # # # ELiminamos los saltos de linea
        # # # for i in range(len(value_amzn_attribute)): 
                
        # # #     value_amzn_attribute[i] = value_amzn_attribute[i].replace('\n','').replace('\t', '').replace('\u200e', '')
            

        # Ubico los atributos con links en su lugar original de la tabla
        for index,name in enumerate(nombres_atributos_amazon):

            if name =='':
                #SI encuentro un espacio vacio, lo elimino
                nombres_atributos_amazon.pop(index)
                try:
                    #reemplazo este espacio eliminado por un atributo con link
                    nombres_atributos_amazon[index] = nombres_attr_with_links[0]
                    #obtengo el atributo con link en la primera posicion de la lista
                    nombres_attr_with_links.pop(0)
                    #elimino este atributo de la primera posicion para la siguiente iter.

                except:

                    continue
        


        #GUARDO LOS NOMBRES Y LOS VALORES COMO STRINGS, USO @ como SEPARADOR
        names_attributes = ''
        attributesDict =  {}
        for name in nombres_atributos_amazon:

            match = re.search("(amazon|ASIN|Precio|Is Discontinued By Manufacturer|Envío nacional|Envío internacional|Garantía|Opinión)",name,re.IGNORECASE)
            if match:
                pass #ignore todo lo que contenga la palabra amazon
            else:
                
                selectorGenerico = "table.prodDetTable tr:contains('"+ str(name) + "') td::text"
                #print(selectorGenerico)
                try: 
                    valueTemporal = response.css(selectorGenerico).get().replace('\n','').replace('\t', '').replace('\u200e', '').strip()
                except:
                    #table#technicalSpecifications_section_1
                    selectorGenerico = "table#technicalSpecifications_section_1 tr:contains('"+ str(name) + "') td::text"
                    try:
                        valueTemporal = response.css(selectorGenerico).get().replace('\n','').replace('\t', '').replace('\u200e', '').strip()
                    except:
                        valueTemporal = ''

                if valueTemporal != '':
                    match = re.search("amazon|http|www|Precio:",valueTemporal,re.IGNORECASE)
                    if match:
                        pass #contiene la palabra amazon, www, Precio:, entonces no se guarda 
                    else:
                        if names_attributes == '':
                            names_attributes = names_attributes + name + ' : ' + valueTemporal
                        else:
                            names_attributes = names_attributes + '/@' + name + ' : ' + valueTemporal

                        attributesDict[name + ':  '] = valueTemporal

        #values_attributes = ''
        # for value in value_amzn_attribute:

        #     if values_attributes == '':
        #         values_attributes = values_attributes + value
        #     else:
        #         values_attributes = values_attributes + '/@' + value


        try:
            print(f'Atributos Scraped amazon: {attributesDict}')
            #print(f'valores de los atributos amazon: {values_attributes}')
        except:
            print('Error... no attributes scrapeados.')

    except:
        names_attributes = "null"
        attributesDict =  {}

    if names_attributes == "":
        names_attributes = "null"

    try:
        attributesDict['Marca:  '] = attributesDict['Fabricante:  ']
        del attributesDict['Fabricante:  ']
        print(f'Atributos Scraped amazon Modificado: {attributesDict}')
    except:
        pass
             
    return  names_attributes,attributesDict 
# actualizacion 14/08/2021
# CON LOS NAME ATTRIBUTES SCRAPEADOS, SE BUSC[O] LA
# CONTRAPARTE, ES DECIR LOS VALUE, CONSTRUYENDO REGEX
# PARA ENCONTRAR CADA UNO, DE ESTA MANERA, CADA
# NAME TIENE SU VALUE CORRESPONEIDNTE.
# SE IGNORARON TODOS LOS NAME CON LA PALABRA AMAZON,
# ASIN, PRECIO.

# # #     # Tabla - Atributos Values - Selectores
# # #     name_amzn_atribute = response.css('table.a-keyvalue th::text').getall()
# # #     nombres_with_links = response.css('table.a-keyvalue th span[style="white-space: normal"]::text ').getall()
# # #     print(f'Nombres with links: {nombres_with_links}')
# # #     # Values 
# # #     value_amzn_atribute = response.css('table.a-keyvalue td::text').getall()


# # #     #print(f'TABLA DE ATRIBUTOS PRODUCTO AMAZON {value_amzn_atribute}')
# # #     long_values = len(value_amzn_atribute)
# # #     long_names = len(name_amzn_atribute)


# # #     print(f'\n\nLong_Names: {long_names}, Long_Values: {long_values}\n\n')
# # #     print(f'\n\nNames: {name_amzn_atribute},Values: {value_amzn_atribute}\n\n')

  
# # #     # Data to Yield
# # #     for i in range(long_names): 

# # #         name_amzn_atribute[i] = name_amzn_atribute[i].replace('\n','')
                

# # #    # Data to Yield
# # #     for i in range(long_values): 
            
# # #         value_amzn_atribute[i] = value_amzn_atribute[i].replace('\n','')
        
  
# # #     for index,name in enumerate(name_amzn_atribute):
# # #         if name =='':
# # #             name_amzn_atribute.pop(index)
# # #             try:
# # #                 name_amzn_atribute[index] = nombres_with_links[0]
# # #                 nombres_with_links.pop(0)
# # #             except:
# # #                 continue


# # #     for index,value in enumerate(value_amzn_atribute):
# # #         if value =='':
# # #             value_amzn_atribute.pop(index)
  
             

# # #     print(f'NAMES SIN VACIOS: {name_amzn_atribute}')
# # #     print(f'VALUES SIN VACIOS: {value_amzn_atribute}')



# # #     #print(f'name_amzn_atribute {name_amzn_atribute}\n')
# # #     #print(f'value_amzn_atribute {value_amzn_atribute}')

# # #     # # # Depuramos los atributos scrapeados de amazon
# # #     # # # eliminamos los valores vacios
# # #     # # for index,value in enumerate(value_amzn_atribute):

# # #     # #     if value != '' and value != sku:
            
# # #     # #         valor.append(value)
# # #     # #         name.append(name_amzn_atribute[index])
# # #     # #         nombre_test = name_amzn_atribute[index]
# # #     # #         #print(f'{nombre_test}: {value}')
            
            
# # #     # #     elif value == sku:

# # #     # #         continue

# # #     # #     else:

# # #     # #         break   

# # #     # # #print(f'\nname: {name}, value: {valor}\n')     

# # #     caracteristicas = ''

# # #     for i in range(len(name_amzn_atribute)):
# # #         caracteristicas = caracteristicas + name_amzn_atribute[i] + ": " + value_amzn_atribute[i] + "\n"
    
# # #     #print(f'\n- Caracteristicas: \n{caracteristicas}')

# # #     return caracteristicas