# Last-updated 24/05/2021
# Se debe crear una funcion para categoria de productos ***
# Definimos el json que se enviara a la API
# En este json ya no se envia la descripcion de las nuevas publicaciones
# La descripcion se envia con un POST diferente
# En caso de querer editar luego la description se debe usar put


# - BODY GENERATOR -
def body_generator(title,category_id,cop,available_quantity,sku,MANUFACTURING_TIME,WARRANTY_TIME,imagenes,attributes):
    body = {
        "title": title, #OK
        "category_id": category_id,  #  #OK
        "price": int(cop),  #OK
        "currency_id": "COP",  #OK
        "available_quantity": int(available_quantity), #OK 
        "buying_mode": "buy_it_now", #OK
        "condition": "new",  #OK
        "listing_type_id": "gold_special", #OK Fijar - Clásica gold_special  #gold_pro Premium
        "seller_custom_field": sku, #OK
        "video_id": "s6S5x4OWrOk", #Video Presentacion Just Market # Fijar
        "sale_terms": [
            {
                "id": "MANUFACTURING_TIME",
                "value_name": MANUFACTURING_TIME, #OK
            },
            {
                "id": "WARRANTY_TYPE",
                "value_name": "Garantía del vendedor"   #OK FIjar
            },
            {
                "id": "WARRANTY_TIME",
                "value_name": WARRANTY_TIME,  #Calcular depende del price
            }
        ],
        #"shipping":{"free_shipping": True},
        "pictures": imagenes,  #OK
        "attributes": attributes,  #OK
    }
    return body

# Fin de la funcion body_generator ----------------------


# Codigo utilizado en la publicacion manual de titeres y relojes
# en los inicios de codificacion de la aplicacions

# # - BODY TITERES -
# def titeres(data, imagenes):
#     body = {
#         "title": data['title'],
#         "category_id": data['category_id'],  # 'MCO176682',
#         "price": int(data['price']),
#         "currency_id": "COP",
#         "available_quantity": int(data['available_quantity']),
#         "buying_mode": "buy_it_now",
#         "condition": "new",
#         "listing_type_id": data['listing_type_id'],
#         "seller_custom_field": data['SELLER_SKU'],
#         "sale_terms": [
#             {
#                 "id": "MANUFACTURING_TIME",
#                 "value_name": data['MANUFACTURING_TIME'],
#             },
#             {
#                 "id": "WARRANTY_TYPE",
#                 "value_name": "Garantía del vendedor"
#             },
#             {
#                 "id": "WARRANTY_TIME",
#                 "value_name": data['WARRANTY_TIME'],
#             }
#         ],
#         "pictures": imagenes,
#         # "0": "BRAND", OK
#         # "1": "MODEL", OK
#         # "2": "CHARACTER", OK
#         # "3": "ANIMAL",  OK
#         # "4": "SET", OK
#         # "5": "PIECES_PER_SET", OK
#         # "6": "PUPPET_TYPE", OK
#         # "7": "MIN_RECOMMENDED_AGE", OK
#         # "8": "LENGTH", OK
#         "attributes": [
#             {
#                 "id": "SELLER_SKU",
#                 "value_name": data['SELLER_SKU']
#             },
#             {
#                 "id": "BRAND",
#                 "value_name": data['BRAND']
#             },
#             {
#                 "id": "MODEL",
#                 "value_name": str(data['MODEL'])
#             },
#             {
#                 "id": "LENGTH",
#                 "value_name": data['LENGTH']
#             },
#             {
#                 "id": "MIN_RECOMMENDED_AGE",
#                 "value_name": data['MIN_RECOMMENDED_AGE'],
#             },
#             {
#                 "id": "PUPPET_TYPE",
#                 "value_name": "Titere de mano"
#             },
#             {
#                 "id": "SET",
#                 "value_name": "No"
#             },
#             {
#                 "id": "PIECES_PER_SET",
#                 "value_name": "0"  # "0"
#             },
#             {
#                 "id": "CHARACTER",
#                 "value_name": "CHARACTER"
#             },
#             {
#                 "id": "ANIMAL",
#                 "value_name": "ANIMAL"
#             }
#         ]
#     }
#     return body

#     # Fin de la funcion titeres -------------------

# # - BODY RELOJES DE PULSO -
# def relojes_pulso(data, imagenes):
#     body = {
#         "title": data['title'], #OK
#         "category_id": data['category_id'],  # 'MCO1442', #OK
#         "price": int(data['price']),  #OK
#         "currency_id": "COP",  #OK
#         "available_quantity": int(data['available_quantity']), #OK
#         "buying_mode": "buy_it_now", #OK
#         "condition": "new",  #OK
#         "listing_type_id": data['listing_type_id'], #OK Fijar
#         "seller_custom_field": data['SELLER_SKU'], #OK
#         "video_id": "WG-j_8BJWC0", #Video Presentacion Just Watches # Fijar
#         "sale_terms": [
#             {
#                 "id": "MANUFACTURING_TIME",
#                 "value_name": data['MANUFACTURING_TIME'], #OK
#             },
#             {
#                 "id": "WARRANTY_TYPE",
#                 "value_name": "Garantía del vendedor"   #OK FIjar
#             },
#             {
#                 "id": "WARRANTY_TIME",
#                 "value_name": data['WARRANTY_TIME'],  #Calcular depende del price
#             }
#         ],
#         "pictures": imagenes,  #OK

#         # "0": "BRAND", OK
#         # "1": "LINE", NO
#         # "2": "MODEL",  OK
#         # "3": "ALPHANUMERIC_MODEL", NO
#         # "4": "GENDER",  OK
#         # "5": "STRAP_COLOR",  OK
#         # "6": "BEZEL_COLOR",  OK
#         # "7": "BACKGROUND_COLOR", OK
#         # "8": "CASE_COLOR", OK
#         # "9": "STRAP_MATERIAL", OK
#         # "10": "DIAL_HOURS_COLOR", NO
#         # "11": "DIAL_MINUTES_SECONDS_COLOR", NO
#         # "12": "NEEDLES_COLOR", NO
#         # "13": "SUBDIALS_COLOR", NO
#         # "14": "LIGHT_COLOR", NO
#         # "15": "DETAILED_MODEL", OK
#         # "16": "MOVEMENT_TYPE",  OK
#         # "17": "DISPLAY_TYPES",  OK
#         # "18": "CASE_MATERIALS", OK
#         # "19": "IS_WATER_RESISTANT", OK

#         # "variations": [{  # Crear variacion

#         #     "available_quantity": int(data['available_quantity']),
#         #     "price": int(data['price']),
#         #     "sold_quantity":100,
#         #     "attribute_combinations": [
#         #         #Atributos que tienen el tag allow_variations=true
#         #         {
#         #             "id": "BACKGROUND_COLOR", #color de fondo
#         #             "value_name": data['BACKGROUND_COLOR'],
#         #         },
#         #         {
#         #             "id": "BEZEL_COLOR", #color bisel
#         #             "value_name": data['BEZEL_COLOR']
#         #         },
#         #     ],
#         #     # Hay que enviar los ids de las imagnes
#         #     "picture_ids": ["690795-MCO41415481406_042020", "633843-MCO43720172147_102020"],
#         #     "attributes":[{
#         #     # se debenenviar los atributos que quiero que tenga la variacion
#         #     # no puedo enviar el mismo atributo en el item y en la variacion
#         #         "id": "SELLER_SKU",
#         #         "value_name": data['SELLER_SKU']
#         #     }]

#         # }],

#         "attributes": [
#             {
#                 "id": "SELLER_SKU",
#                 "value_name": data['SELLER_SKU']  #OK
#             },
#             {
#                 "id": "BRAND",
#                 "value_name": data['BRAND']
#                 # "value_name": None,
#                 # "value_id" : "-1"
#             },
#             {
#                 "id": "MODEL",
#                 "value_name": str(data['MODEL'])  #str
#                 # "value_name": None,
#                 # "value_id" : "-1"
#             },
#             {
#                 "id": "GENDER",
#                 "value_name": data['GENDER']  # Genero
#                 # "value_name": None,
#                 # "value_id" : "-1"
#             },
#             # {
#             #     "id": "STRAP_COLOR", #color correa
#             #     #"hierarchy": "CHILD_PK",
#             #     "tags": {
#             #             "allow_variations": True,
#             #             "defines_picture": True
#             #     },
#             #     "value_name": data['STRAP_COLOR']
#             # },
#             {
#                 "id": "STRAP_COLOR",  # color correa
#                 "value_name":data['STRAP_COLOR']
#                 #"value_name": None,
#                 #"value_id": "-1"
#             },
#             {
#                 "id": "BEZEL_COLOR",  # color bisel
#                 "value_name": data['BEZEL_COLOR']
#                 # "value_name": None,
#                 # "value_id" : "-1"
#             },
#             {
#                 "id": "BACKGROUND_COLOR",  # color de fondo
#                 "value_name": data['BACKGROUND_COLOR']
#                 # "value_name": None,
#                 # "value_id" : "-1"
#             },
#             {
#                 "id": "CASE_COLOR",  # Color de la caja
#                 "value_name": data['CASE_COLOR']
#                 #"value_name": None,  # data['CASE_COLOR']
#                 #"value_id": "-1"
#             },
#             {
#                 "id": "STRAP_MATERIAL",  # Material correa
#                 "value_name": data['STRAP_MATERIAL']
#                 # "value_name": None,
#                 # "value_id" : "-1"
#             },
#             {
#                 "id": "DETAILED_MODEL",
#                 "value_name": data['DETAILED_MODEL']
#                 #"value_name": None,  # data['DETAILED_MODEL'] #Modelo detallado
#                 #"value_id": "-1"
#             },
#             {
#                 "id": "MOVEMENT_TYPE",  # Movimiento, cuarzo..
#                 "value_name": data['MOVEMENT_TYPE']
#                 #"value_name": None,
#                 #"value_id": "-1"
#             },
#             {
#                 "id": "DISPLAY_TYPES",
#                 "value_name": data['DISPLAY_TYPES'] #tipo de pantalla,analoga
#                 #"value_name": None,
#                 #"value_id": "-1"
#             },
#             {
#                 "id": "CASE_MATERIALS",  # Materiales caja, lista
#                 "value_name": data['CASE_MATERIALS']
#                 #"value_name": None,
#                 #"value_id": "-1"
#             },
#             {
#                 "id": "IS_WATER_RESISTANT",
#                 "value_name": data['IS_WATER_RESISTANT'] #resistencia H2O, 50m 100m..
#                 #"value_name": None,
#                 #"value_id": "-1"
#             }
#         ]
#     }
#     return body

#     # Fin de la funcion relojes de pulso ----------------------

# # - BODY RELOJES DE PULSO 2 PRUEBAS -
# def relojes_pulso_2(data, imagenes):

#     # "0": "BRAND", OK
#     # "1": "LINE", NO
#     # "2": "MODEL",  OK
#     # "3": "ALPHANUMERIC_MODEL", NO
#     # "4": "GENDER",  OK
#     # "5": "STRAP_COLOR",  OK
#     # "6": "BEZEL_COLOR",  OK
#     # "7": "BACKGROUND_COLOR", OK
#     # "8": "CASE_COLOR", OK
#     # "9": "STRAP_MATERIAL", OK
#     # "10": "DIAL_HOURS_COLOR", NO
#     # "11": "DIAL_MINUTES_SECONDS_COLOR", NO
#     # "12": "NEEDLES_COLOR", NO
#     # "13": "SUBDIALS_COLOR", NO
#     # "14": "LIGHT_COLOR", NO
#     # "15": "DETAILED_MODEL", OK
#     # "16": "MOVEMENT_TYPE",  OK
#     # "17": "DISPLAY_TYPES",  OK
#     # "18": "CASE_MATERIALS", OK
#     # "19": "IS_WATER_RESISTANT", OK

#     atributos_body = [{'id': 'BRAND', 'name': 'Marca', 'value_name': data['BRAND']},
#                       {'id': 'MODEL', 'name': 'Modelo','value_name': str(data['MODEL'])},
#                       {'id': 'GENDER', 'name': 'Género','value_name': data['GENDER']},
#                       {'id': 'STRAP_COLOR','name': 'Color de la correa','value_name': data['STRAP_COLOR']},
#                       {'id': 'BEZEL_COLOR','name': 'Color del bisel','value_name': data['BEZEL_COLOR']},
#                       {'id': 'BACKGROUND_COLOR','name': 'Color del fondo','value_name': data['BACKGROUND_COLOR']},
#                       {'id': 'CASE_COLOR','name': 'Color de la caja','value_name': data['CASE_COLOR']},
#                       {'id': 'STRAP_MATERIAL','name': 'Material de la correa','value_name': data['STRAP_MATERIAL']},
#                       {'id': 'DETAILED_MODEL','name': 'Modelo detallado','value_name': data['DETAILED_MODEL']},
#                       {'id': 'MOVEMENT_TYPE','name': 'Tipo de movimiento','value_name': data['MOVEMENT_TYPE']},
#                       {'id': 'DISPLAY_TYPES','name': 'Tipos de pantalla','value_name': data['DISPLAY_TYPES']},
#                       {'id': 'CASE_MATERIALS','name': 'Materiales de la caja','value_name': data['CASE_MATERIALS']},
#                       {'id': 'IS_WATER_RESISTANT','name': 'Es resistente al agua','value_name': data['IS_WATER_RESISTANT']}]

#     body = {
#         "title": data['title'],
#         "category_id": data['category_id'],  # 'MCO1442',
#         "price": int(data['price']),
#         "currency_id": "COP",
#         "available_quantity": int(data['available_quantity']),
#         "buying_mode": "buy_it_now",
#         "condition": "new",
#         "listing_type_id": data['listing_type_id'],
#         "seller_custom_field": data['SELLER_SKU'],
#         "sale_terms": [
#             {
#                 "id": "MANUFACTURING_TIME",
#                 "value_name": data['MANUFACTURING_TIME'],
#             },
#             {
#                 "id": "WARRANTY_TYPE",
#                 "value_name": "Garantía del vendedor"
#             },
#             {
#                 "id": "WARRANTY_TIME",
#                 "value_name": data['WARRANTY_TIME'],
#             }
#         ],
#         "pictures": imagenes,

#         "attributes": atributos_body
#     }
#     return body

#     # Fin de la funcion relojes de pulso ----------------------

# # NOTAS ULTIMA VERSION
# # Se traslad[o] la publicacion de las descripciones de los items
# # al programa principal api_publicador
# # para hacerlo mas liviano, ordenado, no redundante
# # Se identifico la seccion del body, que es igual para todas las
# # categorias. Tambien se identifico los atributos que son variables
# # cada categoria tiene atributos diferentes

# # NOTAS 12/03/2021
# # Se aprendio a deshabilitar un atributo N/A
# # se hace uso de value_name : None y Value_id : "-1"
# # Se aprendio acerca de las variaciones
# # Para efectos practicos no haremos uso de las variaciones
# # en este programa.
# # se dejo un trozo de codigo comentado con parte del trabajo
# # hecho con las variaciones.
# # para mayor info consultar documentacion de mercadolibre developers
