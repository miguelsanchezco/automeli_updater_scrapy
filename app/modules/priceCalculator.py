''' 
    Price Calculator 1.0
    by @miguelsanchezco
    Updated: 27/10/2021
    Colombia

    Description: This is a very important module. This module try 
    to model the price extracted from Amazon in the local currency 
    - Colombian peso.
    Using data like: Price in USD, Seller, Shipping From,
    Weigth, Volumen, largest dimmension, taxes, feeds 
    aproximately shipping cost.
'''

''' Modules  and Libraries '''
import re
import math
# from modules.trmCalculator import  trmGetValue


# TRM = trmGetValue()
# print('TRM en priceCalculator.py: ',TRM)

# # # LIMITE_PESO = 80 # Libras

###factorDownload() # Descargo los Factores !
# FACTOR_HIGH,FACTOR_MEDIUM,FACTOR_LOW,FACTOR_WOO = factorGetValues() # Leo los factores !

''' Main fucntion '''

# Si estoy actualizando precios, pasar valor de maxWeigth
# Si estoy scrapeando el producto por primera vez, enviar maxWeigth = 0

def priceCalculator(response, maxWeigth,use_locker,meli_site_id):    
    
    ''' [Paso 0.] Extraer precio en Dolares '''

    try:

        USD = 0    
        list_prices = response.css('div#corePrice_feature_div span.a-offscreen::text').get()
        #response.css('span#price_inside_buybox::text').get()

        if list_prices:
            print('\n1. Selector de precio\n')
            # Si capturamos el precio con el primer selector
            #price = (response.css('span#price_inside_buybox::text').
            #         re("([0-9]+,[0-9]+|[0-9]+\.)"))
            price = (response.css('div#corePrice_feature_div span.a-offscreen::text').
                     re("(\d{1,3}(\.|,)\d+)"))
            print(price)
            #price = ''.join(price).replace(".","") #convertimos lista en string
            #price = price.replace(",","") #Eliminamos (,) o (.)
            #exit = 1
        else:

            list_prices = response.css('span.apexPriceToPay span.a-offscreen::text').get()

            if list_prices:
                # En caso de que el primer selector de price falle
                print('\n2. Selector de precio\n')
                #price = (response.css('span#priceblock_ourprice::text').
                #         re("([0-9]+,[0-9]+|[0-9]+\.)"))
                price = (response.css('span.apexPriceToPay span.a-offscreen::text').
                         re("(\d{1,3}(\.|,)\d+)"))
                #print(price)
                #price = ''.join(price).replace(".","") 
                # #Con esta linea convierto la list en str y reemplzo . por ""
                #price = price.replace(",","") #reemplazo , por ""
            else:
                print('\n3. Selector de precio\n')
                price = (response.css('input#attach-base-product-price::attr(value)').
                         re("(\d{1,3}(\.|,)\d+)"))
                #print(price)

        n_items = len(price)
        #price es una lista de 1, 2 o 4 elementos.

        if n_items == 2:
            #El valor buscado esta en la posicion 0
            USD = price[0].replace(",","") #eliminamos las (,) Precios >999USD
        elif n_items == 4:
            #El valor buscado esta en la posicion 2
            USD = price[2].replace(",","") #eliminamos las (,) Precios >999USD
            USD_2 = price[0].replace(",","") #Productos que tienen valor x Onza, tienen 2 precios, Example: 7USD/Ounce
            try:
                if float(USD_2)> float(USD): #Validamos que el USD_2 no sea mayor que USD
                    USD = USD_2              #SI es mayor, asiganmos USD como USD_2
                    print('Producto con dos precios, se toma el mas alto!!!')
            except:
                pass
        else:
            print('Item sin precio!')
            USD = 0 # para informar que no se publique el item
            
        #price = '' #Limpiamos price
        USD = float(USD)  # le asignamos a price el valor de USD flotante
        print(f'Precio RE: {USD} USD')    
        #price = int(price)
    
    except ValueError as e:
        print("\n** ValueError in Selectores_css **\n")
        USD = 0 #USD


    except TypeError as e:
        print("\n** TypeError in Selectores_css **\n")
        USD = 0 #USD
  

    # if USD < 35:
    #     FACTOR = FACTOR_HIGH  # 1 - 34.99 USD
    # elif USD >= 35 and USD < 70:
    #     FACTOR = FACTOR_MEDIUM  #35 - 69.99 USD
    # elif USD >= 70 :
    #     FACTOR = FACTOR_LOW  # >70 USD
    
    

    ''' [Paso 1.] Extraer peso y volumen '''
            
    weigth =  re.search('(\d{1,3}(\.|)\d+) Onzas',response.text)  
    try:  
        print(f'weigth: {weigth.group(0)}')
        weigth = weigth.group(0)
    except:
        weigth =  re.search('(\d{1,3}(\.|)\d+) onzas',response.text)  
        try:
            print(f'weigth: {weigth.group(0)}')
            weigth = weigth.group(0)
        except:
            weigth =  re.search('(\d{1,3}(\.|)\d+) Libras',response.text) 
            try:
                print(f'weigth: {weigth.group(0)}')
                weigth = weigth.group(0)
            except:
                weigth =  re.search('(\d{1,3}(\.|)\d+) pounds',response.text) 
                try:
                    print(f'weigth: {weigth.group(0)}')
                    weigth = weigth.group(0)
                except:
                    weigth = 'null'
        
    #VOLUMEN
    #\d+(\.\d+|) x \d+(\.\d+|) x \d+(\.\d+|) (.*?)(?=\s)                       
    volume =  re.search('\d+(\.\d+|) x \d+(\.\d+|) x \d+(\.\d+|)(.*?)(?=)',response.text)
    try:  
        print(f'volume: {volume.group(0)}')
        volume = volume.group(0)
    except:
        volume = 'null'
        print(f'volumen: {volume}\n')
    volin3 = volume #volumen 0.0 X 0.0 X 0.0 in3

    ''' [Paso 2.] Preguntar si existe peso, volumen y maxWeigth'''

    if weigth == 'null' and volume == 'null' and maxWeigth == 0:
        #print('Si no hay Precio ni Volumen, no publicar o no activar!')
        weigth = '20 Libras' # No hay informacion de weigth and volume
        # Para envitar problemas con el price, ponemos peso maximo.
    

    ''' [Paso 3.] Calculamos peso volumetrico '''
    
    pesoVol = 0

    if volume != 'null':
        
        # si volumen diferente de null
        # ejemplo: 1 x 2 x 3 pulgadas
        volume = volume.split(' ')
        # convierto volumen en una lista
        try:
            volume.pop(1) # elimino la x
            volume.pop(2) # elimino la x
            for i in range(3):
                volume[i] = math.ceil(float(volume[i])*2.54)
            pesoVol = math.ceil(((volume[0]*volume[1]*volume[2])/5000)*2.2)
            print(f'PESO VOLUMETRICO {pesoVol} lbs')
        except:
            print('Error al calcular peso Volumetrico.')

    ''' [Paso 4.] Eliminamos las unidades de peso, Onzas to Lb'''

    if weigth != 'null':
            #SI peso diferente de null
            weigth = weigth.split(' ')
            unidad_peso = weigth.pop() # unidad de peso
            weigth = weigth[0]           # valor peso
            print(f'PESO: {weigth} {unidad_peso}')
            if unidad_peso == 'Onzas' or unidad_peso == 'onzas':
                weigth = math.ceil(float(weigth)*0.0625) #libras
            else:
                weigth = math.ceil(float(weigth)) #Redondeamos arriba
            print(f'PESO*: {weigth} libras')

    ''' [Paso 5.] Determinamos el peso mayor '''
  
    
    if weigth == 'null':
        weigth = 0
    if volume == 'null':
        pesoVol = 0

    if maxWeigth > 0 and (maxWeigth == weigth or maxWeigth == pesoVol):   #YA EXISTEEEEEEEEEEEEEE maxWeigth
        
        print('No hacer nada, peso max. Ya Existe! y sigue igual')
        
    else:
        print('peso no existe en DB o cambio de valor.')
        try:
            print(f'peso max antes : {maxWeigth}')
        except:
            print('error maxWeigth antes no existe')

        # No existe, se calcula.
        if weigth >= pesoVol:
            maxWeigth = weigth
           
        else:
            maxWeigth = pesoVol
           
        
        
    print(f'maxWeigth = {maxWeigth}\n')
 
    
    # if maxWeigth > LIMITE_PESO: # SI el peso del proeducto es mayor a 40lbs
    #         USD = 0 # No venderlo en Meli o pausarlo

    ''' [Paso 6.] Hallamos EnviadoPor y VendidoPor'''

    # # # #VENDIDO Y ENVIADO POR <<< <<< <<<
    despachador = 'null'
    vendedor = 'null'
    
    despachador = response.css('div.tabular-buybox-text span::text').get()
    vendedor = response.css('div.tabular-buybox-text span a::text').get()
    
    if vendedor == None:
        try:
            match = re.search("Amazon", despachador)
            print(f'match2 vendedor: amazon')
            vendedor = 'Amazon'
           
        except:
            print('No Matches')
            vendedor = 'null'

    if despachador == None:
        despachador = 'null'
        
    #Vendedor ---
    match = re.search("Amazon Global",vendedor)
    if match:
        vendedor = 'amazonGlobal' #Amazon Europa
    else:
        match = re.search("Amazon",vendedor)
        if match:
            vendedor = 'amazon'
        else:
            vendedor = 'otro'

    #Despachador ---
    match = re.search("Amazon Global",despachador)
    if match:
        despachador = 'amazonGlobal'
    else:
        match = re.search("Amazon",despachador)
        if match:
            despachador = 'amazon'
        else:
            despachador = 'otro'
            

    #vendedor = response.css('div.tabular-buybox').get()

    #vendedor = response.css('div.tabular-buybox-label span::text').get() 

    #print(f'\n\n*****Vendedor: {vendedor}, Despachador: {despachador}*****\n\n')
    #VENDIDO Y ENVIADO POR <<< <<< <<<

    ''' [Paso 6.2] Determinamos si el envio es GRATIS '''

    # freeShipping = response.css('span#freeShippingPriceBadging_feature_div')
    # print('freeShipping : ',freeShipping)
    #TABLE
    table = response.css('table.a-lineitem td.a-span2 span::text').getall()
    print('tablee10: ',table)
    
    #Inicializamos variables
    tableTotalUSD = USD
    tableShippingCost = 0
    tableTaxes = 0
    tableTotalUSD = USD
    freeShipping35USD = False
    #Extraemos datos y depuramos
    if table != []:
        tableUSD = float(table[0].replace('US$','').replace(',',''))
        tableShippingCost = float(table[1].replace('US$','').replace(',',''))
        tableTaxes = float(table[2].replace('US$','').replace(',',''))
        tableTotalUSD = float(table[3].replace('US$','').replace(',',''))
        print('tableUSD: ',tableUSD)
        print('shippingCost: ',tableShippingCost)
        print('taxes: ',tableTaxes)
        print('tableTotalUSD: ',tableTotalUSD)
        #SI el precio scrapeado es menor que el de la tabla, se usa el de la tabla.
        if USD < tableUSD:
            print(f'Precio USD: {USD} cambiado a tableUSD: {tableUSD}')
            USD = tableUSD

    #ENVIO GRATIS COMPRAS MAYORES A 35
    condicionalEnvioGratis = response.css('span[data-csa-c-mir-sub-type="CONDITIONALLY_FREE"]')
    print('condicional ',condicionalEnvioGratis)
    if condicionalEnvioGratis != []:
        freeShipping35USD = True
        print('Envios Gratis por compras mayores a 35USD: ',freeShipping35USD)
        

    ''' [Paso 7.] Calculamos shippingCost y taxes '''
    shippingCost = 10   #Inicializo shippingCost en caso de que no 
    #                    se escrapee info de vendedor y despachador

    if(meli_site_id == 'MLC'):

        if USD <= 30:
            taxes = 0       #Inicializo taxes
        else:
            taxes = USD*0.28 

    elif(meli_site_id == 'MEC'):

        if USD <= 400:
            taxes = 0
        else:
            taxes = USD*0.15
    
    elif(meli_site_id == 'MLA'):
         
        if USD <= 50:
            taxes = 1.9*USD
        elif USD >50 and USD <100:
            taxes = 1.6*USD
        elif USD>100 and USD<500:
            taxes = 1.25*USD
        else:
            taxes = 1.1*USD

    elif(meli_site_id == 'MCO' or meli_site_id == 'MPE'):

        if USD <= 200:
            taxes = 0       #Inicializo taxes
        else:
            taxes = USD*0.27


    elif(meli_site_id == 'MLM'):

        if USD <= 50:
            taxes = 0 
        elif USD >50 and USD<1000:
            taxes = USD*0.18      #Inicializo taxes
        else:
            taxes = USD*0.26 

    else:

        taxes = USD*0.27 

    #''' AMAZON - AMAZON '''
    #if vendedor == 'amazon' and despachador == 'amazon':

    #if USD < 200: #and maxWeigth < 9: # <200USD and <9lbs.

    if table == [] and USD>0 and use_locker == 1:
        #No envian a colombia, toca casillero.
        print('Toca por Casillero! ')
        if(meli_site_id == 'MCO'):

            #ECUACIONES SE SACAN DE COSTO DE CASILLERO
            if USD < 200 and maxWeigth < 9:
                shippingCost = 2.5*maxWeigth + 18
                taxes = USD*0.13 #TAXES PARA ENVIAR AL CASILLERO
            elif USD < 200 and maxWeigth >= 9: #<200USD and >9lbs.
                taxes = USD*0.13  #TAXES PARA ENVIAR AL CASILLERO
                if maxWeigth <= 13:
                    shippingCost = 2.52*maxWeigth + 20
                else:
                    shippingCost = 2.54*maxWeigth + 23
            
            elif USD >= 200 and maxWeigth < 9: #>200USD and <9lbs
                shippingCost = 2.5*maxWeigth + 18
                taxes = USD*0.33

            elif USD >=200 and maxWeigth >= 9: #>200USD and >9lbs
                shippingCost = 2.52*maxWeigth + 20
                if maxWeigth > 35:
                    shippingCost = 4.70*maxWeigth - 55 
                taxes = USD*0.33

        elif(meli_site_id == 'MLM'):
            USD = 0
        elif(meli_site_id == 'MLA'):
            USD = 0
        elif(meli_site_id == 'MLC'):
            USD = 0
        elif(meli_site_id == 'MPE'):
            USD = 0
        elif(meli_site_id == 'MEC'):
            USD = 0

    elif table != []: 

        if freeShipping35USD == False:
            shippingCost = tableShippingCost
        else:
            shippingCost = 0
        
        taxes = tableTaxes

    else:
        #print('el usuario no tiene activo el uso de casillero')
        USD = 0 #No se usa casillero. No se puede vender en Mercadolibre.
        shippingCost = 0 
    # # #     elif USD < 200 and maxWeigth >= 9: #<200USD and >9lbs.
    # # #         if maxWeigth <= 13:
    # # #             shippingCost = 2.52*maxWeigth + 20
    # # #         else:
    # # #             shippingCost = 2.54*maxWeigth + 23
            
    # # #     elif USD >= 200 and maxWeigth < 9: #>200USD and <9lbs
    # # #         shippingCost = 0
    # # #         taxes = USD*0.3

    # # #     elif USD >=200 and maxWeigth >= 9: #>200USD and >9lbs
    # # #         shippingCost = 2.52*maxWeigth + 20
    # # #         if maxWeigth > 35:
    # # #             shippingCost = 4.70*maxWeigth - 55 
    # # #         taxes = USD*0.33

    # # # # OTRO - AMAZON
    # # # elif vendedor == 'otro' and despachador == 'amazon':

    # # #     if USD < 200 and maxWeigth < 9: # <200USD and <9lbs.
    # # #         if USD < 35:
    # # #             shippingCost = 7
    # # #         else:
    # # #             shippingCost = 0
           
    # # #     elif USD < 200 and maxWeigth >= 9: #<200USD and >=9lbs.
    # # #         if maxWeigth<21:
    # # #             shippingCost = 4.1*maxWeigth - 3.65
    # # #         else:
    # # #             shippingCost = 3.13*maxWeigth + 35.12
            
    # # #     elif USD >= 200 and maxWeigth >= 9:#>200USD and >=9lbs
    # # #         shippingCost = 1.95085883E+02-1.42377129E+00*maxWeigth+5.31540958E-03*maxWeigth **2 - 3.15909112E-02*USD+5.77324241E-06*USD **2
    # # #         taxes = 0.33*USD

    # # #     elif USD >= 200 and maxWeigth < 9:
    # # #         shippingCost = 0
    # # #         taxes = 0.27*USD

    # # # # OTRO - OTRO 
    # # # elif vendedor == 'otro' and despachador == 'otro':
    # # #     print('Este Producto no se envia a Colombia, no se activará...')
    # # #     USD = 0

    # # # # GLOBAL - GLOBAL
    # # # elif vendedor =='amazonGlobal' and despachador == 'amazonGlobal':

    # # #     if USD < 200 and maxWeigth < 9: # <200USD and <9lbs.
    # # #         shippingCost = 35
           
    # # #     elif USD < 200 and maxWeigth >= 9: #<200USD and >9lbs.
    # # #         if maxWeigth <= 13:
    # # #             shippingCost = 2.52*maxWeigth + 20
    # # #         else:
    # # #             shippingCost = 2.54*maxWeigth + 23
        
    # # #     elif USD >= 200 and maxWeigth < 9: #>200USD and <9lbs
    # # #         shippingCost = 35
    # # #         taxes = USD*0.45

    # # #     elif USD >=200 and maxWeigth >= 9: #>200USD and >9lbs
    # # #         shippingCost = 2.52*maxWeigth + 20
    # # #         if maxWeigth > 35:
    # # #             shippingCost = 4.70*maxWeigth - 55 
    # # #         taxes = USD*0.45

    # # # # OTRO - GLOBAL
    # # # elif vendedor == 'otro' and despachador == 'amazonGlobal':

    # # #     if USD < 200 and maxWeigth < 9: # <200USD and <9lbs.
    # # #         shippingCost = 45
         
    # # #     elif USD < 200 and maxWeigth >= 9: #<200USD and >9lbs.
    # # #         shippingCost = 2.52*maxWeigth + 20
    # # #         if maxWeigth > 35:
    # # #             shippingCost = 4.70*maxWeigth - 55
            
    # # #     elif USD >= 200 and maxWeigth < 9: #>200USD and <9lbs
    # # #         shippingCost = 45
    # # #         taxes = USD*0.45

    # # #     elif USD >=200 and maxWeigth >= 9: #>200USD and >9lbs
    # # #         shippingCost = 2.52*maxWeigth + 20
    # # #         if maxWeigth > 35:
    # # #             shippingCost = 4.70*maxWeigth - 55 
    # # #         taxes = USD*0.45 

    
    ''' [Paso 8.] Calculamos el precio total en Moneda de Amazon '''
    
    if USD>0:
        print(f'shippingCost: {shippingCost}\ntaxes: {taxes}')
        USD_total = USD + shippingCost + taxes  #Precio en dolares sumando tax + shipping
    else:
        USD_total = 0
        shippingCost = 0
        taxes = 0
    
    #MELI
    #usd_converted = USD_total * TRM # * FACTOR # Precio de venta en Meli CO
    #WOOCOMMERCE
    #regular_price_woo = USD_total * TRM # * FACTOR_WOO
    USD_total = float("{:.2f}".format(USD_total))
    shippingCost = float("{:.2f}".format(shippingCost))
    taxes = float("{:.2f}".format(taxes))
    
    print(f'USD: {USD} + ShippingCost: {shippingCost} + taxes: {taxes} = {USD_total}')
    
    #usd_converted redondeado 990
    # usd_converted = (math.ceil(usd_converted/1000) * 1000) - 10
    #regular_price_woo redondeado 990
    # regular_price_woo = (math.ceil(regular_price_woo/1000) * 1000) - 10
    
    # if usd_converted < 79990: # SI hay un precio inferior a 79mil, setearlo en 79mil
    #     usd_converted = 79990 # Para ofrecer Envio gratis y que salga mas barato 
    #     regular_price_woo = 70000

    # if USD == 0: #Si no se scrapero precio USD
    #     usd_converted = 0
    #     regular_price_woo = 0
    
    # print(f'usd_converted: {usd_converted}')
    # print(f'regular_price_woo: {regular_price_woo}')

    if maxWeigth == '':
        maxWeigth = 0

    
    return USD, weigth, volin3, pesoVol, maxWeigth, USD_total,vendedor,despachador, shippingCost, taxes 
    
    # NOTAS
    # PENDIENTE:
    # pendiente revisar selector cuando el  vendedor es otro 
    # y despachador Amazon GLobal.