
from modules.mysqlCRUD import DataLogManager
import math
import json

def priceFactorsConversion(usd_total,seller_id,databaseName,meli_site_id):
    
    ''' Creo un Objeto para conexión con BaseDeDatos'''
    objectDataLog = DataLogManager(databaseName)
    dataUser = objectDataLog.extractUserData(seller_id)  #Trae parameters
    TRM  = dataUser.loc[0,'trm']
    jsonstring = dataUser.loc[0,'json']
    # factor_range_1 = float(dataUser.loc[0,'factor_range_1'])
    # factor_range_2 = float(dataUser.loc[0,'factor_range_2'])
    listJson = json.loads(jsonstring)
 
    # if usd_total < factor_range_1:
    #     FACTOR = dataUser.loc[0, "factor_high_meli"]  # 1 - 49.99 usd_total
    #     FACTOR_MSHOPS = dataUser.loc[0, "factor_high_mshops"]
    # elif usd_total >= factor_range_1 and usd_total < factor_range_2:
    #     FACTOR = dataUser.loc[0, "factor_medium_meli"]   #50 - 99.99 usd_total
    #     FACTOR_MSHOPS = dataUser.loc[0, "factor_medium_mshops"]
    # elif usd_total >= factor_range_2:
    #     FACTOR = dataUser.loc[0, "factor_low_meli"]   # >100 USD
    #     FACTOR_MSHOPS = dataUser.loc[0, "factor_low_mshops"]
    FACTOR = ''
    FACTOR_MSHOPS = ''
    for item in listJson:
        
        if usd_total>=item['min'] and usd_total<item['max']:
            print(item)
            FACTOR = (item['meli']/100)+1
            FACTOR_MSHOPS = (item['mshops']/100)+1
            meli_price = usd_total * FACTOR * TRM
            mshops_price = usd_total * FACTOR_MSHOPS * TRM
            break
        
    if FACTOR == '' and FACTOR_MSHOPS == '':
        FACTOR = 2
        FACTOR_MSHOPS = 2
        meli_price = usd_total * FACTOR * TRM
        mshops_price = usd_total * FACTOR_MSHOPS * TRM
    
    print("FACTOR_MSHOPS: ", FACTOR_MSHOPS)

    print(f'meli_priceeee:  USD {usd_total} ,FACTOR {FACTOR} , TRM {TRM}')

    # meli_price =  usd_total * FACTOR * TRM
    # mshops_price = usd_total * FACTOR_MSHOPS * TRM
    
    print(f'meli_priceeee antes redondeo: {meli_price}')
    
    #REDONDEOS
    if meli_site_id == 'MCO' or meli_site_id=='MLC' :
        decima = 10 #colombia
    else:
        decima = 1 #argentina, mexico, ecuador, Perú

    if meli_price < 100:
        decima = 0,1  #modena dolares. ejemplo ecuador
    if meli_price >=100 and meli_price < 1000: 
        divisor = 1
    elif meli_price >= 1000 and meli_price < 50000:
        divisor = 10
    elif meli_price >= 50000 and meli_price < 100000: 
        divisor = 100
    elif meli_price >= 100000: 
        divisor = 1000
   
    
    meli_price = (math.ceil(meli_price/divisor) * divisor) - decima if meli_price != 0 else meli_price
    mshops_price = (math.ceil(mshops_price/divisor) * divisor) - decima if mshops_price != 0 else mshops_price
    
    print(f'meli_priceeee despues redondeo: {meli_price}')

    return meli_price, mshops_price