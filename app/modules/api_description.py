# Crear un Modulo que genere la descripcion del producto
# 05/06/2022
# Natalia Pinilla & Miguel Sanchez 


import os
# path = os.getcwd() + '/tmp/'
# path_text_down = path + "text_down.txt"
# path_text_up = path + "text_up.txt"

def description_creator(titleOriginal, titleNew, caracteristicas,description_final,dataUser):  #title,caracteristicas,texto,texto2

    encabezado1 = f"\nTÍTULO: \n{titleOriginal}\n"#\nSKU: {sku}"
    encabezado2 = f"\nTÍTULO: \n{titleNew}\n"
    #title_sku = "Este es el titulo. \nSKU: B0938848"
    #caracteristicas = "peso: pesado jeje\n aroma : lindu\n"
    #importamos la descripcion creada por nati
    # # with open(path_text_down, 'r') as file:
    #print(f'encabezado1: {encabezado1}')        
    # #     text_down = file.read()
    text_down = dataUser.loc[0,'text_down']
    # # #importamos la advertencia inicial
    # # with open(path_text_up, 'r') as file:
            
    # #     text_up = file.read()
    text_up = dataUser.loc[0,'text_up']
    #texto = "Hola, SOy texto 1mjejeje\n salto de linea texto 1 jejeje"
    #texto2 = "Hola SOy texto 2 jejeje bbois\n salto de linea texto 2. xD"

    if caracteristicas != '':
        caracteristicas = "\nTABLA DE CARACTERÍSTICAS:\n" + caracteristicas

    if len(description_final) > 10:
        description_final = "\nDETALLES:" + description_final
    else: 
        description_final = ''

    descripcion = ['']*7
    descripcion[0] = text_up + encabezado1 + description_final  + caracteristicas + "\n\n" + text_down
    descripcion[1] = text_up + "\n" + description_final  + caracteristicas + "\n\n" + text_down
    descripcion[2] = text_up + encabezado1  + caracteristicas + "\n\n" + text_down
    descripcion[3] = text_up + caracteristicas + "\n\n" + text_down
    descripcion[4] = text_up + encabezado1 + "\n" + text_down
    descripcion[5] = text_up + encabezado2 + "\n" + text_down
    descripcion[6] = text_up + "\n\n" + text_down

    return  descripcion #print(f'descripcion: {descripcion}')

# if __name__ == "__main__":

#     print("antes")
#     description_creator()
#     print("despues")