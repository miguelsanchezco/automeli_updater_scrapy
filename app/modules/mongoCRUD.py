
from datetime import datetime
from pymongo import MongoClient

def mongoSaveProduct(sku ,amazon_site, site_id, seller_id, meli_sale_price, meli_regular_price, scraped_price, stock_quantity, shippingCost, taxes, title, images, id_meli_category, currencyMeli, geo_result_id):
#   mongoSaveProduct(sku ,'amazon.com', self.meli_site_id, self.seller_id,  meli_price, scraped_price, available_quantity, shippingCost ,taxes , '' , {}, '', '' )
    client = MongoClient("mongodb+srv://justmarketco:IAtd0PM41q9YBPUL@automelimong0.etafi.mongodb.net/automeli?retryWrites=true&w=majority")
    db = client['automeli']
    collectionProducts = db['products']
    date =  str(datetime.now()).split(".")[0]
    sale_price = meli_sale_price
    regular_price = meli_regular_price

    if amazon_site == 'amazon.com':
        currencyAmzn = 'USD'
    elif amazon_site == 'amazon.com.mx':
        currencyAmzn = 'MXN'
    else:
        currencyAmzn = 'USD'

    #Eliminamos las imagenes que no son de amazon
    # listImages = []
    # for image in images:
    #     if 'images/I/' in image['source']:
    #         listImages.append(image) 

    # images = listImages


    #DOCUMENTO A INSERTAR TIPO 1
    # newDocument =  {"sku":sku,
    #                 "title":title,
    #                 "amazon_sites":[
    #                     { 
    #                         "amazon_site": amazon_site,
    #                         "site_id": site_id,
    #                         "currency": currencyAmzn,
    #                         "history_prices": [{ "date":date, "price":scraped_price, "shipping_cost":shippingCost, "taxes":taxes, "stock_quantity":stock_quantity}],
    #                         "date_created":date  
    #                     }  
    #                 ],
    #                 "sellers":[{
    #                     "id":seller_id,
    #                     "site_id":site_id,
    #                     "amazon_site":amazon_site,
    #                     "id_meli_category": id_meli_category,
    #                     "currency": currencyMeli,
    #                     "history_prices":[
    #                         { "date":date,
    #                         "sale_price":sale_price,
    #                         "regular_price":regular_price,
    #                         "stock_quantity":stock_quantity}
    #                         ],
    #                     "date_created":date
    #                 }],
    #                 "pictures":images,
    #                 "date_created":date,
    #                 "date_updated":date
                    
    #             }

    #DOCUMENTO TIPO 2
    # newSeller =    {
    #                     "id":seller_id,
    #                     "site_id":site_id,
    #                     "amazon_site":amazon_site,
    #                     "id_meli_category": id_meli_category,
    #                     "currency": currencyMeli,
    #                     "history_prices":[
    #                         { "date":date,
    #                         "sale_price":sale_price,
    #                         "regular_price":regular_price,
    #                         "stock_quantity":stock_quantity
    #                         }
    #                     ],
    #                     "date_created":date
    #                 }

    #DOCUMENTO TIPO 3
    newPricesSeller = {     
                            "date":date,
                            "sale_price":sale_price,
                            "regular_price":regular_price,
                            "stock_quantity":stock_quantity
                      }

    #DOCUMENTO TIPO 4. precios de amazon
    newPricesSiteId = { "date":date, "price":scraped_price, "shipping_cost":shippingCost, "taxes":taxes, "stock_quantity":stock_quantity}

    #DOCUMENTO TIPO 5. Objeto precios de amazon
    # newAmazonObject =   { 
    #                         "amazon_site": amazon_site,
    #                         "site_id": site_id,
    #                         "currency": currencyAmzn,
    #                         "history_prices": [{ "date":date, "price":scraped_price, "shipping_cost":shippingCost, "taxes":taxes, "stock_quantity":stock_quantity}],
    #                         "date_created":date  
    #                     }


    ## LOGICA ##

    # Escenario 1. Documento No existente. 
    # PRIMERO PREGUNTAR si EXISTE
    # query = {"sku":sku}
    # response = collectionProducts.find_one(query)
    # #print('Mongo Step 1: ',response)
    # if response==None:
    #     #creamos el documento tipo 1
    #     print('No existe Documento. Lo Creamos')
    #     response = collectionProducts.insert_one(newDocument)
    #     print('acknowledged:',response.acknowledged)
    #     print('inserted_id:',response.inserted_id)
       
    # else:
        
        # # #AGREGAMOS prices de amazon segun amazon_site and  geo_result_id
    query = {"sku":sku, "amazon_sites.amazon_site":amazon_site, "amazon_sites.site_id":geo_result_id }
        # response = collectionProducts.find_one(query)
        # #print(response)
        # if response == None:
        #     #SI no existe record para ese amazon_site con ese site_id, lo creamos
        #     #Se agrega al array docuemnto 5
        #     response = collectionProducts.update_one({"sku":sku} , {'$push':{"amazon_sites":newAmazonObject}})
        # else:
        #     #Ya existe record. entonces se agrega los precios al array price_history. documento 4
    response = collectionProducts.update_one(query,{"$addToSet":{"amazon_sites.$.history_prices":newPricesSiteId}})
    
    print('Mongo Step 2. Agregamos precio a Sites Amazon, acknowledged:',response.acknowledged)

    #Ya existe SKU. revisamos el seller
    # print('Mongo Step 3: Ya existe SKU, revisamos si existe seller')
    # query = {"sku":sku, "sellers.id":seller_id}
    # response = collectionProducts.find_one(query,{"sellers":1})
    # #print(response)

    # if response==None:
    #     #No existe seller_id. lo creamos
    #     print("Mongo Step 4.1 No existe seller_id. lo creamos")
    #     query = {"sku":sku}
    #     response = collectionProducts.update_one(query,{ "$push": {"sellers":newSeller}})
    #     print(' Creado con exito ? acknowledged:',response.acknowledged)
    # else:
    #Ya existe el seller, agregamos precios nuevos!
    print('Mongo Step 4.2: Ya existe el seller, agregamos nuevo precio si no esta repetido!')
    
    query = {"sku":sku, "sellers.id":seller_id}
    response = collectionProducts.update_one(query,{"$addToSet":{"sellers.$.history_prices":newPricesSeller}})
    print('acknowledged:',response.acknowledged)
            
