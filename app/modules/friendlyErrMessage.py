
def friendlyErrMessage(errMessage):

    if 'The attributes [GTIN]' in errMessage:
        return 'Se requiere Identificador Universal del Producto: GTIN'
    
    elif 'Currency null' in errMessage:
        return 'Error de Moneda. Por favor conctácte al soporte de Automeli'

    elif 'seller.unable_to_list' in errMessage:
        return 'Tu cuenta de MercadoLibre no esta habilitada para publicar.'

    elif 'Validation error' in errMessage:
        return 'Error de validacion. Este producto no se puede publicar.'
    elif 'Item without price' in errMessage:
        return 'Item sin precio o no se envia a tu pais. Revisa si tienes la opcion casillero activa'
    
    else:
        return  errMessage.split('.')[0]  
