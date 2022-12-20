
from datetime import datetime
from pymongo import MongoClient

def mongoSaveProduct(sku ,amazon_site, site_id, seller_id, meli_price, scraped_price, stock_quantity, shippingCost, taxes, title, images, id_meli_category, currencyMeli):
    client = MongoClient("mongodb+srv://justmarketco:IAtd0PM41q9YBPUL@automelimong0.etafi.mongodb.net/automeli?retryWrites=true&w=majority")
    db = client['automeli']
    collectionProducts = db['products']
    date =  str(datetime.now()).split(".")[0]
    sale_price = meli_price
    regular_price = meli_price

    if amazon_site == 'amazon.com':
        currencyAmzn = 'USD'
    elif amazon_site == 'amazon.com.mx':
        currencyAmzn = 'MXN'
    else:
        currencyAmzn = 'USD'

    #Eliminamos las imagenes que no son de amazon
    listImages = []
    for image in images:
        if 'images/I/' in image['source']:
            listImages.append(image) 

    images = listImages


    #DOCUMENTO A INSERTAR TIPO 1
    newDocument =  {"sku":sku,
                    "title":title,
                    "amazon_sites":[
                        { 
                            "amazon_site": amazon_site,
                            "site_id": site_id,
                            "currency": currencyAmzn,
                            "history_prices": [{ "date":date, "price":scraped_price, "shipping_cost":shippingCost, "taxes":taxes, "stock_quantity":stock_quantity}],
                            "date_created":date  
                        }  
                    ],
                    "sellers":[{
                        "id":seller_id,
                        "site_id":site_id,
                        "amazon_site":amazon_site,
                        "id_meli_category": id_meli_category,
                        "currency": currencyMeli,
                        "history_prices":[
                            { "date":date,
                            "sale_price":sale_price,
                            "regular_price":regular_price,
                            "stock_quantity":stock_quantity}
                            ],
                        "date_created":date
                    }],
                    "pictures":images,
                    "date_created":date,
                    "date_updated":date
                    
                }

    #DOCUMENTO TIPO 2
    newSeller =    {
                        "id":seller_id,
                        "site_id":site_id,
                        "amazon_site":amazon_site,
                        "id_meli_category": id_meli_category,
                        "currency": currencyMeli,
                        "history_prices":[
                            { "date":date,
                            "sale_price":sale_price,
                            "regular_price":regular_price,
                            "stock_quantity":stock_quantity
                            }
                        ],
                        "date_created":date
                    }

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
    newAmazonObject =   { 
                            "amazon_site": amazon_site,
                            "site_id": site_id,
                            "currency": currencyAmzn,
                            "history_prices": [{ "date":date, "price":scraped_price, "shipping_cost":shippingCost, "taxes":taxes, "stock_quantity":stock_quantity}],
                            "date_created":date  
                        }


    ## LOGICA ##

    # Escenario 1. Documento No existente. 
    # PRIMERO PREGUNTAR si EXISTE
    query = {"sku":sku}
    response = collectionProducts.find_one(query)
    print('Mongo Step 1: ',response)
    if response==None:
        #creamos el documento tipo 1
        print('No existe Documento. Lo Creamos')
        response = collectionProducts.insert_one(newDocument)
        print('acknowledged:',response.acknowledged)
        print('inserted_id:',response.inserted_id)
       
    else:
        
        # # #AGREGAMOS prices de amazon segun amazon_site and  site_id
        query = {"sku":sku, "amazon_sites.amazon_site":amazon_site, "amazon_sites.site_id":site_id }
        response = collectionProducts.find_one(query)
        print(response)
        if response == None:
            #SI no existe record para ese amazon_site con ese site_id, lo creamos
            #Se agrega al array docuemnto 5
            response = collectionProducts.update_one({"sku":sku} , {'$push':{"amazon_sites":newAmazonObject}})
        else:
            #Ya existe record. entonces se agrega los precios al array price_history. documento 4
            response = collectionProducts.update_one(query,{"$addToSet":{"amazon_sites.$.history_prices":newPricesSiteId}})
        
        print('Mongo Step 2. Agregamos precio a Sites Amazon, acknowledged:',response.acknowledged)

        #Ya existe SKU. revisamos el seller
        print('Mongo Step 3: Ya existe SKU, revisamos si existe seller')
        query = {"sku":sku, "sellers.id":seller_id}
        response = collectionProducts.find_one(query,{"sellers":1})
        print(response)

        if response==None:
            #No existe seller_id. lo creamos
            print("Mongo Step 4.1 No existe seller_id. lo creamos")
            query = {"sku":sku}
            response = collectionProducts.update_one(query,{ "$push": {"sellers":newSeller}})
            print(' Creado con exito ? acknowledged:',response.acknowledged)
        else:
            #Ya existe el seller, agregamos precios nuevos!
            print('Mongo Step 4.2: Ya existe el seller, agregamos nuevo precio si no esta repetido!')
           
            query = {"sku":sku, "sellers.id":seller_id}
            response = collectionProducts.update_one(query,{"$addToSet":{"sellers.$.history_prices":newPricesSeller}})
            print('acknowledged:',response.acknowledged)
            


    

    # # # # #Paso 1. Creo el documento si no existe
    # # # # url = "https://ddjzxplzv0.execute-api.us-east-1.amazonaws.com/api/productos/create-product"

    # # # # payload = json.dumps({
            
    # # # #     "site_id": site_id, 
    # # # #     "sku": sku, 
    # # # #     "seller_id": seller_id, 
    # # # #     "amazon_site": amazon_site

    # # # # })

    # # # # headers = {
    # # # # 'Content-Type': 'application/json'
    # # # # }

    # # # # while True:
    # # # #     response = requests.request("POST", url, headers=headers, data=payload)
    # # # #     print('MongoResultCreationDocument:',response.text)
    # # # #     print('status',response.status_code)
    # # # #     if response.status_code == 200 or response.status_code == '200':
    # # # #         break

    # # # # #Paso 2. Enviamos Precios
    # # # # url = "https://ddjzxplzv0.execute-api.us-east-1.amazonaws.com/api/productos/create-mongo-product"


    # # # # payload = json.dumps({
    # # # #     "site_id": site_id,
    # # # #     "sku": sku,
    # # # #     "seller_id": seller_id,
    # # # #     "amazon_site": amazon_site,
    # # # #     "regPrice":meli_price,
    # # # #     "salePrice":0,
    # # # #     "stock_quantity":stock,
    # # # #     "amazonPrice": total_price
    # # # # })
    # # # # headers = {
    # # # # 'Content-Type': 'application/json'
    # # # # }

    # # # # while True:
    # # # #     response = requests.request("POST", url, headers=headers, data=payload)
    # # # #     print('MongoResultUpdatedPrices:',response.text)
    # # # #     print('status',response.status_code)
    # # # #     if response.status_code == 200 or response.status_code == '200':
    # # # #         break


    # # # # # # seller_id = 2222222   
    # # # # # # #collectionProducts.insert_one(productInfo)
    # # # # # # # result = collectionProducts.find_one(myquery)
    # # # # # # amazon_site = amazon_site.split('.')[-1]
    # # # # # # date =  str(datetime.now()).split(".")[0]
    # # # # # # # newHistoryPrice = {'date': date, 'regPrice': meli_price, 'salePrice': 0, 'amazonPrice': total_price}
    # # # # # # newProductObject = {
    # # # # # #         'sku': sku,
    # # # # # #         "amazon_sites": {

    # # # # # #             amazon_site: {

    # # # # # #                 site_id: {

    # # # # # #                     "data":[{
    # # # # # #                         "seller_id":seller_id,
    # # # # # #                         "history_prices": [{
    # # # # # #                             "date":date,
    # # # # # #                             "regPrice":meli_price,
    # # # # # #                             "salePrice":0,
    # # # # # #                             "stock_quantity":stock
    # # # # # #                         }]
    # # # # # #                     }],
    # # # # # #                     "history_scraped_price":[{
    # # # # # #                         "date":date,
    # # # # # #                         "amazonPrice": total_price,
    # # # # # #                         "stock_quantity":stock
    # # # # # #                     }]
    # # # # # #                 }
    # # # # # #             }

    # # # # # #         }
    # # # # # # }

    
    # # # # # # print('newProductObject: ',newProductObject)
    # # # # # # myquery = {'sku':sku}
    # # # # # # collectionProducts.update_one(myquery, {'$push': newProductObject}, upsert=True)
    
    #collectionProducts.insert_one(newProductObject)
    #else:
    # newvalues = { "$push": { "history_prices": newHistoryPrice}} 
    # datePrices.update_one(myquery, newvalues)