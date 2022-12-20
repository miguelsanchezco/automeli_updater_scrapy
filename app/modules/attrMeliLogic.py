import re
import random

def attrMeliLogic(i,atributos,body_attr,attributesDict,brand,model,weight):

    attr_dict = {}
    # Atributo NO oculto
    attr_dict['id'] = atributos[i]['id']

    #test = attr_dict['id']
    #print(f'\nATRIBUTO NO OCULTO: {test} \n')

    # pregunto si el atributo es de tipo str, list, int, bool ,...          
    attribute_type = atributos[i]['value_type']
    #print(f'Atribute Type: {attribute_type}')
    
    try:
        # Reviso si el atributo tiene unidades obligatorias
        default_unit = atributos[i]['default_unit']
        #print(f'\nDEFAULT UNITS: {default_unit} \n')
        units = 1
        # units = 1 significa que requiere unidades.
    except: 
        # No tiene unidades
        #print('Dont have default_unit')
        units = 0
    
    bandera = 0
    data_name = atributos[i]['name']
    
    if attr_dict['id'].lower()=='brand':
        data_name = brand
    elif attr_dict['id'].lower()=='model' or  attr_dict['id'].lower()=='line':
        data_name = model

    # LLENADO AUTOMATICO DE ATRIBUTOS SCRAPEADOS #############
    for clave in attributesDict:
        #recorro diccionario de atributos scrapeados de amazon
        #print(f"{atributos[i]['name'].lower()} in  {clave.lower()} ")
        if  clave.lower() in atributos[i]['name'].lower() or  atributos[i]['name'].lower() in clave.lower():
            #print(f'Yupiii2: {clave}')

            if units == 1:
                #miramos si el atributo tiene numeros
                Number =  re.search('\d+',attributesDict[clave])  #mejorar regex para coger decimales!!!
                
                try:
                    Number = Number.group(0)
                    #print(f'Original: {attributesDict[clave]}, Just Number: {Number}, attribute_type: {attribute_type}') 
                    bandera = 1
                    data_name = Number
                except:
                    data_name = attributesDict[clave]
            else:
                data_name = attributesDict[clave]   

            break

       
    # GTIN, vamos a pasar un N/A para este atributo en un producto que lo exige.
    # Logitech G533 Parlantes Inalámbricos Para Juegos Dts 71. Producto de Catalogo
    

    if attr_dict['id']=='GTIN':
        #continue
        attr_dict['value_name'] = None
        attr_dict['value_id'] = '-1'
        # almaceno en bpdy_attr el diccionario que se acabo de crear.  
        body_attr.append(attr_dict)
       

    elif attr_dict['id']=='WEIGHT':
        #continue
        attr_dict['value_name'] = str(int(weight/2.2)) + ' kg' 
        
        # almaceno en bpdy_attr el diccionario que se acabo de crear. 
        body_attr.append(attr_dict)
    
    elif attr_dict['id']=='GENDER':
        #continue
        attr_dict['value_name'] = 'Sin género' 
        
        # almaceno en bpdy_attr el diccionario que se acabo de crear. 
        body_attr.append(attr_dict)
    

    else:
        # Si es un atributo diferente a GTIN y no es oculto.
        # Lo guardo !
        #data_name = attr_dict['name']
        # Almaceno en data_name el nombre del atributo.
        if attribute_type == 'number':
            attr_dict['value_name'] = 0
        # Pregunto si el atributo type es booleano o tipo numero
        elif attribute_type == 'boolean':
            # si es booleano, envio a meli un N/A
            #print(f'dataName: {data_name}')
            try:
                if atributos[i]['tags']['required']:
                    attr_dict['value_name'] = 'No'  
            except:  
                attr_dict['value_id'] = '-1'
                attr_dict['value_name'] = None
                
            # else:
            #PROVISIONALLLLLLLLLLLLL  - no se si funciona
            #attr_dict['value_id'] = str(random.randint(242084, 242085))
            #random.choice([True, False])  #---mas lento


        elif attribute_type == 'string' or attribute_type == 'list':
            # si el atributo es de tipo string o list envio el data_name
            if units == 1:
                # pregunto si tiene unidades obligatorias.
                attr_dict['value_name'] = data_name + ' ' + default_unit
            else:
                # si no tiene unidades envio unicamente el data_name
                if attribute_type == 'string':
                    attr_dict['value_name'] = data_name
                else:
                    # si no tiene unidades y es list, pongo N/A
                    #attr_dict['value_name'] = atributos[i]['values'][0]['name']  #list
                    attr_dict['value_name'] = 'Ver Descripción'
                    # attr_dict['value_id'] = '-1'

        elif attribute_type == 'number_unit':
            # si el atributo es de tipo numero, envio numero.
            if units == 1:
                # pregunto si tiene unidades obligatorias.
                if bandera == 0:
                    attr_dict['value_name'] = '0' + ' ' + default_unit
                else:
                    attr_dict['value_name'] = Number + ' ' + default_unit #posible Bugg por las unidades !!!
            else:
                attr_dict['value_name'] = 0
        else:
            # Tipo de atributo desconocido. envio N/A a mercadolibre
            # No es list, number, boolean, number_init 
            try:
                if atributos[i]['tags']['required']:
                    attr_dict['value_name'] = 'No'  
            except:  
                attr_dict['value_name'] = None #No Modificar Valores
                attr_dict['value_id'] = '-1'   #No Modificar Valores

        # almaceno en bpdy_attr el diccionario que se acabo de crear.  
        body_attr.append(attr_dict)

       

    return body_attr