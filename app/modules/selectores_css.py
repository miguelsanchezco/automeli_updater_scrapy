'''
    # Nymeliapp Version2.0
    # Modulo para extraer precio, disponibilidad de stock
    # y envio a colombia
    # requiere la response obtenida al scrapear un producto
    # de amazon
    # Miguel Sanchez R.
    # @miguelsanchezco
    # 8/12/2021 
'''

from modules.priceCalculator import priceCalculator
from datetime import datetime
import re

# Para su uso en DataSpider, enviar maxWeigth=0
def selectores_css(response,maxWeigth,mtactive,mtauto,mtdays,use_locker,meli_site_id):

    # shipping_cost = (response.
    # css('div#exports_desktop_qualifiedBuybox_tlc_feature_div span.a-size-base::text').
    # get() #.re('[0-9]+')[0])
    # print(f"\n\n\n Shipping_cost GET : {shipping_cost} \n\n\n")
    # # Cuando no hay costo de envio, el toma el mismo precio del producto.
    # if shipping_cost:
    #     shipping_cost = (response.
    #     css('div#exports_desktop_qualifiedBuybox_tlc_feature_div span.a-size-base::text').
    #     re('[0-9]+')[0])
    #     shipping_cost = int(shipping_cost)
    #     print(f"\n\n\n Shipping_cost: {shipping_cost} \n\n\n")

    # Logica para establecer precio en usd_converted
    
    #Crear funcion para cálulo del precio
    [USD,weigth,volume,pesoVol,maxWeigth, USD_total,
     vendedor,despachador,shippingCost,taxes] = priceCalculator(response,maxWeigth,use_locker,meli_site_id)
    
    # country , Geolocalizacion 
    try:
        country = response.css('span#glow-ingress-line2::text').get().replace("\n","")
    except:
        country = 'null'

    if country:
        country = country.replace('\u200e','').replace('\t', '').replace('  ','').strip()
        #.replace(' ','')
        print(f'country:{country}\n')
    

    #Si el producto tiene precio, USD!=0, verificar disponibilidad de stock
    if USD != 0: 
        
        try:
            stock = response.css('div#availability span::text').get().replace("\n","")  
        except:
            print('No stock information. se seteara como Disponible el x dia')
            stock = "Disponible el x dia"  
    else:
        # si el producto no tiene precio, USD=0, poner available_quantity en 0
        stock = 'No disponible'

    if len(stock) < 10:
        print('Sin informacion de Stock, se seteara como Disponible el x dia')    
        stock = 'Disponible el x dia'
    #print(f"Disponibilidad: {stock},\ncountry:{country}\n") # Para pruebas

    #  Logica para determinar disponibilidad de Stock
        # No se envia a colombia, Usar Casillero
    print(f'STOCK INFO: {stock} , longitud: {len(stock)}')
    match = re.search("Disponible el",stock)
    if match:
        available_quantity = 1
        MANUFACTURING_TIME = '15 dias'
    else:
        match = re.search("No disponible",stock)
        if match:
            available_quantity = 0
            MANUFACTURING_TIME = '30 dias'
        else:
            match = re.search("Envío en",stock)
            if match:
                available_quantity = 1
                MANUFACTURING_TIME = '15 dias'
            else:
                match = re.search("Sólo hay",stock)
                if match:
                    available_quantity = 1
                    MANUFACTURING_TIME = '15 dias'  ## null
                else:
                    match = re.search("Solo queda",stock)
                    if match:
                        available_quantity = 1
                        MANUFACTURING_TIME = '15 dias'  ## null
                    else:
                        match = re.search("Disponible.",stock)
                        if match:
                            available_quantity = 3
                            MANUFACTURING_TIME = '15 dias'  ## null
                        else:
                            available_quantity = 0
                            MANUFACTURING_TIME = '30 dias'
                            # No disponible

    #DETERMINAMOS MANUFACTURING TIME ---------------------------------------------------------------------------------------
    delivery_message = response.css('div#mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE span::text').getall()
    print(f'delivery_message {delivery_message}')
    meses = ['ene','feb','marz','abr','may','jun','jul','ago','sep','oct','nov','dic']

    for message in delivery_message:
        for index, mes in enumerate(meses):
            #print(f'mes: {mes} in {message}')
            if mes.lower() in message.lower():
                print('message dayNumber: ', message.lower())
                dayNumber =  re.search('\d+',message) 
                print('dayNumber: ',dayNumber) 
                try:
                    dayNumber = dayNumber.group(0)
                except:
                    dayNumber = '30' #Inventamos
                    
                print(f'Encontrado!! mes: {index+1}, dia: {dayNumber}')
                currenMonth = datetime.now().month
                currenDayNumber = datetime.now().day
                if currenMonth == index+1:
                    MANUFACTURING_TIME = str(int(dayNumber) - int(currenDayNumber)) + ' dias'
                    print(f'MANUFACTURING_TIME  {MANUFACTURING_TIME}') 
                else:
                    MANUFACTURING_TIME = str((31 - int(currenDayNumber)) + int(dayNumber) )+ ' dias'
                    print(f'MANUFACTURING_TIME  {MANUFACTURING_TIME}') 

                break


    if mtactive == 0:
        if available_quantity > 0:
            MANUFACTURING_TIME = '0 dias'

    # elif mtauto == 1:
    #     delivery_message = response.css('div#mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE span::text').getall()
    #     print(f'delivery_message {delivery_message}')
    #     meses = ['ene','feb','marz','abr','may','jun','jul','ago','sep','oct','nov','dic']
    
    #     for message in delivery_message:
    #         for index, mes in enumerate(meses):
    #             #print(f'mes: {mes} in {message}')
    #             if mes.lower() in message.lower():
    #                 print('message dayNumber: ', message.lower())
    #                 dayNumber =  re.search('\d+',message) 
    #                 print('dayNumber: ',dayNumber) 
    #                 try:
    #                     dayNumber = dayNumber.group(0)
    #                 except:
    #                     dayNumber = '30' #Inventamos
                        
    #                 print(f'Encontrado!! mes: {index+1}, dia: {dayNumber}')
    #                 currenMonth = datetime.now().month
    #                 currenDayNumber = datetime.now().day
    #                 if currenMonth == index+1:
    #                     MANUFACTURING_TIME = str(int(dayNumber) - int(currenDayNumber)) + ' dias'
    #                     print(f'MANUFACTURING_TIME  {MANUFACTURING_TIME}') 
    #                 else:
    #                     MANUFACTURING_TIME = str((31 - int(currenDayNumber)) + int(dayNumber) )+ ' dias'
    #                     print(f'MANUFACTURING_TIME  {MANUFACTURING_TIME}') 

    #                 break

    elif mtauto == 0 and mtdays > 0:
        MANUFACTURING_TIME = str(mtdays) + ' dias'
    
        
    #price is a price in USD
    return [USD,available_quantity,MANUFACTURING_TIME,weigth,volume,
            pesoVol,maxWeigth,USD_total,country,vendedor,despachador,
            shippingCost,taxes]