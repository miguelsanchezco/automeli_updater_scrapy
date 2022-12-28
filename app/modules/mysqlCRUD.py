# pip install PyMySQL
# Google SQL Cloud
# proyecto: nymeliapp
# email just....co@g.....com

'''
    updated: 22/05/2022    
    Metodos Base de Datos!
    MySQL en la nube
'''
import time
import pymysql
import pandas as pd
from random import randint
#Conexion a traves de clases
class DataLogManager:


    #Constructor
    def __init__(self, dataBase):
        #Conexion: Google:
        # self.connection = pymysql.connect(
        #     host='35.188.21.4', #ip SQL Cloud mysqltest
        #     user='super_user',  #root
        #     password='bhfsd@1=98712d58M5wUY',  #aj783ndjd@xj**-@>,
        #     db= dataBase,    
        # )

        # Conexión: Amazon:
        self.connection = pymysql.connect(
            host='databasesmysql.cpd9nr0jwueq.us-east-1.rds.amazonaws.com', #ip SQL Cloud mysqltest
            user='justmarketco',  #root
            password='1098763422Ms',  #aj783ndjd@xj**-@>,
            db= dataBase,    
        )
        
        
        self.cursor = self.connection.cursor()
        print("Conexión exitosa!")
        
        
        
    # # OBTENER DATA DE 1 SOLO ITEM O PRODUCTO
    # def selectItemBySku(self,table, sku):
    #     sql = (f"SELECT * FROM {table} WHERE sku = '{sku}'")

    #     try:
    #         self.cursor.execute(sql)
    #         #fetchone porque es 1 solo resultado.
    #         item = self.cursor.fetchone()

    #         #Printeo datos extraidos de la base de datos
    #         print("id:",item[0])
    #         print("sku:",item[1])
    #         print("cop:",item[2])
    #         print("available_q:",item[3])
    #         print("last_updated:",item[4])
    #         print("date_published:",item[5])
    #         print("maxWeigth:",item[6])
    #         print("country:",item[7])
    #         print("meli_account:",item[8])
    #         #self.cursor.close()
    #         self.connection.close()
    #         return item
            
    #     except Exception as e:
    #         raise
    #         #Aun no se ha creado codigo para majear las excep..
    #     finally:
    #             if self.connection.open:
    #                 #self.cursor.close()
    #                 self.connection.close()


    # def extractAllDataByAccount(self,table, ACCOUNT):  #Extraer datos de la Meli_Account X
    #     sql = f"SELECT * FROM {table} WHERE meli_account = {ACCOUNT}"

        
    #     try:
    #         self.cursor.execute(sql)
    #         #fetchall porque son varios resultados o todos
    #         allData = list(self.cursor.fetchall())
    #         longitud = len(allData)
    #         #inicializo las listas
    #         ids=[0]*longitud
    #         skus=[0]*longitud
    #         old_cop = [0]*longitud
    #         old_available_quantity = [0]*longitud
    #         old_last_updated = [0]*longitud
    #         publishedDate = [0]*longitud
    #         oldMaxWeigth = [0]*longitud
    #         i = 0
    #         # guardo la data en las listas, 
    #         # a futuro puede crearse un dataframe
    #         for data in allData:
    #             data = list(data)
    #             ids[i] = data[0]
    #             skus[i] = data[1]
    #             old_cop[i] = data[2]
    #             old_available_quantity[i] = data[3]
    #             old_last_updated[i] = data[4]
    #             publishedDate[i] = data[5]
    #             oldMaxWeigth[i] = data[6]
    #             i = i+1
    #             #print(i)
            
    #         print("OK\n")
    #         #self.cursor.close()
    #         self.connection.close()
    #         return [ids,skus,old_cop, old_available_quantity,
    #                 old_last_updated,publishedDate,oldMaxWeigth]
            
    #     except Exception as e:
    #         raise
    #         #AUn no se ha creado codigo para majear las excep..
    #     finally:
    #             if self.connection.open:
    #                 #self.cursor.close()
    #                 self.connection.close()


    def extractAllDataByMeliAccount(self,ACCOUNT):
        #Solo Datos con cambios => hubo_cambio = 'SI'
        sql = f"""SELECT meli_publications.id_meli_publication, meli_publications.status_publication, products_info.usd_total,
        sku_products.id_sku,sku_products.sku, products_info.usd, products_info.taxes, products_info.cop, products_info.sale_cop, products_info.stock_quantity, 
        meli_publications.date_updated, meli_publications.date_created, products_info.shipping_cost,
        products_info.error_404, products_info.delivery_time, products_info.GTIN  
        FROM ((meli_publications
        INNER JOIN products_info
        ON id_meli_account = {ACCOUNT} AND meli_publications.id_sku = products_info.id_sku and products_info.hubo_cambio != "" AND products_info.real_stock = "NO")
        INNER JOIN sku_products ON sku_products.id_sku = meli_publications.id_sku)"""
        try:
            df = pd.read_sql(sql, self.connection)
            return df

        except Exception as e:
            print(f'hubo un error en extractAllDataByMeliAccount: {e}')
            #raise  
        finally:
                if self.connection.open:
                    ##self.cursor.close()
                    self.connection.close()


    def updateRealStock(self, sku, new_real_stock):
        print(sku, new_real_stock)
        # get id_sku from sku_products
        sql_id_sku = f"SELECT id_sku from sku_products where sku = '{sku}'"
    
        try:
            self.cursor.execute(sql_id_sku)
            id_sku = self.cursor.fetchone()[0]
            print("id_sku: ", id_sku)
            try:
                sql_update_real_stock = f"UPDATE products_info SET real_stock= '{new_real_stock}' WHERE id_Sku = {id_sku}"
                self.cursor.execute(sql_update_real_stock)
                self.connection.commit() #Guarda Cambios
                print(f"real stock updated for {sku}")
            except Exception as e:
                print(f'hubo un error en updateRealStock updating real stock: {e}')
                #raise  
            finally:
                if self.connection.open:
                    ##self.cursor.close()
                    self.connection.close()
        
        except Exception as e:
            print(f'hubo un error en updateRealStock: {e}')
            #raise  
        finally:
                if self.connection.open:
                    ##self.cursor.close()
                    self.connection.close()



    def extractAllData(self, table):  #Extraer datos de la Meli_Account X
        sql = f"SELECT * FROM {table}"
        
        again = 0
        while again == 0:

            try:
                self.cursor.execute(sql)
                #fetchall porque son varios resultados o todos
                allData = list(self.cursor.fetchall())           
                df = pd.DataFrame(allData, columns=["id_woo", "id_meli",	"account_meli","id_sku","sku",	"usd",	"cop_meli",	"sale_price_woo", "regular_price_woo",	
                "stock_quantity","status_meli",	"status_woo", "manufacturing_time",	"date_created_woo",	"date_created_meli",
                "date_modified_woo", "date_modified_meli",	"max_weigth", "error_404", "last_update_amazon"])
                print("OK\n")
                #self.cursor.close()
                self.connection.close()
                return df

                
            except Exception as e:
                #raise
                again = 1
                print("Fallido")
                time.sleep(5)
            finally:
                if self.connection.open:
                    #self.cursor.close()
                    self.connection.close()

            #AUn no se ha creado codigo para majear las excep..  
    


    def updateProducts(self,table, id_value, name_primary_key, **dict_to_update):
        """
        creates a string that is a sql query.
        input:
            table: (str) the name of the table to update 
            id_value: (int) value of the primary_key
            name_primary_key: (str) name of the primary key
            dict_to_update: (dict) the names and values to change in the table. If the type of value of any keyword of
                    dictionary is different of string then the value is not taken as string
            
        output:
            nothing


        usd, cop_meli regular_price_woo sale_price_woo stock_quantity status_meli status_woo
        manufacturing_time date_modified_woo date_modified_meli    
        """
        sql = f"UPDATE {table} SET "
        keys = dict_to_update.keys()
        
        for key in keys:
            if type(dict_to_update[key]) != str:
                sql += f"{key} = {dict_to_update[key]}, "
            else:
                sql += f"{key} = '{dict_to_update[key]}', "
                
        sql = sql[:-2] 

        if type(id_value) != str:     
            sql += f" WHERE {name_primary_key} = {id_value}"
        else:
            sql += f" WHERE {name_primary_key} = '{id_value}'"
        
        #print(sql)
        try:
            self.cursor.execute(sql)
            self.connection.commit() #Guarda Cambios
            #self.connection.close() #cerramosconexion <<<<
            #Persistencia del update, inset o delete
            print('\nRegistro enviado a Base de datos AWS!\n')
        except Exception as e:
            print(f'hubo un error en updateProducts: {e}')
            #raise  
        finally:
                if self.connection.open:
                    ##self.cursor.close()
                    self.connection.close()

    
    def updateAnyTable(self,table, id_value, name_primary_key, **dict_to_update):
        """
        
        """
        sql = f"UPDATE {table} SET "
        keys = dict_to_update.keys()
        
        for key in keys:
            if type(dict_to_update[key]) != str:
                sql += f"{key} = {dict_to_update[key]}, "
            else:
                sql += f"{key} = '{dict_to_update[key]}', "
                
        sql = sql[:-2] 

        if type(id_value) != str:     
            sql += f" WHERE {name_primary_key} = {id_value}"
        else:
            sql += f" WHERE {name_primary_key} = '{id_value}'"
        
        print(sql)
        try:
            self.cursor.execute(sql)
            self.connection.commit() #Guarda Cambios
            #self.connection.close() #cerramosconexion <<<<
            #Persistencia del update, inset o delete
            print('\nRegistro enviado a Base de datos AWS!\n')
        except Exception as e:
            print(f'hubo un error en updateAnyTable: {e}')
            #raise  
        finally:
                if self.connection.open:
                    ##self.cursor.close()
                    self.connection.close()



    def dfToTableDB(self, table, df):
        """
        upload a dataframe to a table in DB. Dataframe must have the same estructure than the DB table

        input:
            table: (str) table in the DB
            df: (DataFrame) values to load in DB table

        output:
            None
        """
        col_names = []        
        for col in df.columns:
            col_names.append(col)

        values = list(df.to_records(index=False))
        values = [tuple(element) for element in values]
        
        s = ["%s"]*len(col_names)
        ss = ",".join(s)
        ss = f"({ss})"

        insert_into = ",".join(col_names)
        insert_into = f"({insert_into})"

        sql = "INSERT INTO {} {} VALUES {}".format(table, insert_into, ss)
        try:
            self.cursor.executemany(sql, values)
            self.connection.commit()

            print(self.cursor.rowcount, f"Record inserted successfully into {table} table")   

        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:
            #if cursor.connection:
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")

    
    def dbTableToDf(self, table):
        try: 
            sql = "SHOW COLUMNS FROM {}".format(table)
            self.cursor.execute(sql)
            columns_info = self.cursor.fetchall()
            col_names = [element[0] for element in columns_info]

            sql = "SELECT * FROM {}".format(table)
            self.cursor.execute(sql)
            #fetchall porque son varios resultados o todos
            allData = list(self.cursor.fetchall()) 
            
            df = pd.DataFrame(allData, columns= col_names)    
            return df

        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:   
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")


    def downloadApiKeysForToday(self):
        try:
            table = "scraperapi"

            sql = "SHOW COLUMNS FROM {}".format(table)
            self.cursor.execute(sql)
            columns_info = self.cursor.fetchall()
            col_names = [element[0] for element in columns_info]
            

            #today = datetime.now().strftime("%d/%m/%Y")
            sql = "SELECT * FROM {}".format(table) # WHERE date_usage = '{}'".format(table, today)
            self.cursor.execute(sql)
            #fetchall porque son varios resultados o todos
            allData = list(self.cursor.fetchall()) 
            
            df = pd.DataFrame(allData, columns= col_names)    
            return df

        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:   
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")

    
    def downloadCookies(self,amazon_site, meli_site, zip_code):
        try:
            table = "cookies"
            sql = f"SELECT * FROM {table} where amazon_site='{amazon_site}' and meli_site='{meli_site}' and status !='expired'" 
            df = pd.read_sql(sql, self.connection)
            cantCookies = df.shape[0]
            print(f'cantidadCookies: {cantCookies}')
            idRandom = randint(0,cantCookies-1)
            cookieDf = df.iloc[idRandom]
            print(f'cookieSelected: {cookieDf}')
            return cookieDf   
            
        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:   
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")


    def downloadTrm(self):
        # para descarga de datos de la tabla trm en bd. Descargar el ultimo trm:
        try:
            table = "trm"
            values_to_extract = "trm"
            sql = "SELECT {} FROM {} ORDER BY id DESC LIMIT 1".format(values_to_extract, table)
            self.cursor.execute(sql)
            trm = self.cursor.fetchone()[0]
            df = pd.DataFrame({"trm": [trm]})
            return df
        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:   
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")

    def downloadFactorMeli(self, ACCOUNT):
        # para descarga de datos de la tabla trm en bd. Descargar el ultimo trm:
       
        sql = f"select FACTOR_HIGH, FACTOR_MEDIUM, FACTOR_LOW, FACTOR_MSHOPS_HIGH, FACTOR_MSHOPS_MEDIUM, FACTOR_MSHOPS_LOW from meli_accounts where id_meli_account = {ACCOUNT}"

        try:                
            df = pd.read_sql(sql, self.connection)
            return df
        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:   
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")

    def planInfo(self, seller_id):
        # para descarga de datos de la tabla trm en bd. Descargar el ultimo trm:
       
        sql = f"select status_account, publisher_available_quantity, publisher_usage, testing_usage, site_id from meli_accounts where seller_id = {seller_id}"

        try:                
            df = pd.read_sql(sql, self.connection)
            return df
        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:   
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")

    def testUser(self, site_id):
        # para descarga de datos de la tabla trm en bd. Descargar el ultimo trm:
       
        sql = f"select * from meli_accounts where name like '%Test%' and site_id='{site_id}';"

        try:                
            df = pd.read_sql(sql, self.connection)
            return df
        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:   
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")

    def downloadFactorWoo(self, ACCOUNT):
        # para descarga de datos de la tabla trm en bd. Descargar el ultimo trm:
       
        sql = f"select FACTOR_WOO_HIGH, FACTOR_WOO_MEDIUM, FACTOR_WOO_LOW from woo_accounts where id_woo_account = {ACCOUNT}"

        try:                
            df = pd.read_sql(sql, self.connection)
            return df
        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:   
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")

    def extractDataByWooAccount(self, account):  #Extraer datos de la Meli_Account X
        # sql = f"""SELECT sku_products.sku, sku_products.id_sku
        #             FROM woo_publications
        #             INNER JOIN sku_products
        #             ON woo_publications.id_sku = sku_products.id_sku and woo_publications.id_woo_account = {account};"""
        

        sql = f"""SELECT sku_products.sku, sku_products.id_sku, products_info.cop, products_info.stock_quantity, 
            woo_publications.id_woo_publication, products_info.sale_cop, products_info.usd_total,
            woo_publications.status_publication, products_info.delivery_time, products_info.max_weigth
            FROM ((woo_publications
            INNER JOIN sku_products ON woo_publications.id_sku = sku_products.id_sku and woo_publications.id_woo_account = {account})
            INNER JOIN products_info ON woo_publications.id_sku  = products_info.id_sku and products_info.hubo_cambio != "" AND products_info.real_stock = "NO");"""

        

        try:           
            df = pd.read_sql(sql, self.connection)            
            return df
            
        except pymysql.Error as error:
            print(error)
            self.connection.rollback()
            print(f"Failed to make query")
        except NameError as error:
            print(error)
        finally:   
            if self.connection.open:
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")

                

    def extractDataByWooAccount2(self, account):  #Extraer datos de la Meli_Account X
        # sql = f"""SELECT sku_products.sku, sku_products.id_sku
        #             FROM woo_publications
        #             INNER JOIN sku_products
        #             ON woo_publications.id_sku = sku_products.id_sku and woo_publications.id_woo_account = {account};"""
        

        sql = f"""SELECT sku_products.sku, sku_products.id_sku, products_info.cop, products_info.stock_quantity, 
            woo_publications.id_woo_publication, products_info.regular_price_woo, products_info.sale_price_woo,
            woo_publications.status_publication, products_info.delivery_time, products_info.max_weigth
            FROM ((woo_publications
            INNER JOIN sku_products ON woo_publications.id_sku = sku_products.id_sku and woo_publications.id_woo_account = {account})
            INNER JOIN products_info ON woo_publications.id_sku  = products_info.id_sku);"""

        again = 0
        while again == 0:

            try:
                self.cursor.execute(sql)
                #fetchall porque son varios resultados o todos
                allData = list(self.cursor.fetchall())           
                #df = pd.DataFrame(allData, columns=["sku", "id_sku"])
                df = pd.DataFrame(allData, columns=["sku", "id_sku","cop", "stock_quantity", "id_woo_publication", "regular_price_woo", "sale_price_woo", "status_publication", "delivery_time", "max_weigth"])
                print("OK\n")
                #self.cursor.close()
                self.connection.close()
                return df

                
            except Exception as e:
                #raise
                again = 1
                print("Fallido: ", e)
                time.sleep(5) 
            finally:
                if self.connection.open:
                    #self.cursor.close()
                    self.connection.close()

    def getRefreshTokenMeli(self, seller_id):
        sql = f"select refresh_token from meli_accounts where seller_id = {seller_id}"

        try:
                self.cursor.execute(sql)
                #fetchall porque son varios resultados o todos
                refresh_token = self.cursor.fetchone()[0]         
                #df = pd.DataFrame(allData, columns=["sku", "id_sku"])                
                self.connection.close()
                return refresh_token

                
        except Exception as e:
            #raise
            print("Fallido RefreshToken mysql: ", e)
            time.sleep(5) 
        finally:
            if self.connection.open:
                #self.cursor.close()
                self.connection.close()

    def updateAccessTokenMeli(self, seller_id, **dict_to_update):
        """
        creates a string that is a sql query.
        input:
            table: (str) the name of the table to update 
            id_sku: (int) the id_sku of the product
            dict_to_update: (dict) the names and values to change in the table. If the type of value of any keyword of
                    dictionary is different of string then the value is not taken as string
            
        output:
            nothing


        usd, cop_meli regular_price_woo sale_price_woo stock_quantity status_meli status_woo
        manufacturing_time date_modified_woo date_modified_meli    
        """
        sql = f"UPDATE meli_accounts SET "
        keys = dict_to_update.keys()
        
        for key in keys:
            if type(dict_to_update[key]) != str:
                sql += f"{key} = {dict_to_update[key]}, "
            else:
                sql += f"{key} = '{dict_to_update[key]}', "
                
        sql = sql[:-2] 
            
        sql += f" WHERE seller_id  = {seller_id}"
        
        
        #print(sql)
        try:
            self.cursor.execute(sql)
            self.connection.commit() #Guarda Cambios
            #self.connection.close() #cerramosconexion <<<<
            #Persistencia del update, inset o delete
            print('\nRefresh y access token actualizados en Base de datos AWS!\n')
        except Exception as e:
            print(f'hubo un error en updateAccessTokenMeli: {e}')
            #raise  
        finally:
                if self.connection.open:
                    ##self.cursor.close()
                    self.connection.close()


    def usageIncrement(self, seller_id, key, credits,**dict_to_update):
        """
           #update meli_accounts set key = key + 1 where seller_id= seller_id;
           Donde key puede ser publisher_usage or testing_usage
        """
        sql = f"UPDATE meli_accounts SET "
        
        sql += f"{key} = {key} + {credits}"
            
        sql += f" WHERE seller_id  = {seller_id}"

        try:
            self.cursor.execute(sql)
            self.connection.commit() #Guarda Cambios
            #Persistencia del update, inset o delete
            print(f'\n+1 {key} Increment!\n')
        except Exception as e:
            print(f'hubo un error en usageIncrement: {e}')
            #raise  
        finally:
                if self.connection.open:
                    ##self.cursor.close()
                    self.connection.close()

    def updateCookies(self, idcookie, name_key, value_key,**dict_to_update):
        """
           
        """
        sql = f"UPDATE cookies SET "
        
        sql += f"{name_key} = '{value_key}'"
            
        sql += f" WHERE idcookie  = {idcookie}"

        try:
            self.cursor.execute(sql)
            self.connection.commit() #Guarda Cambios
            #Persistencia del update, inset o delete
            print(f'\nCookie: {idcookie} Updated!\n')
        except Exception as e:
            print(f'hubo un error en usageIncrement: {e}')
            #raise  
        finally:
                if self.connection.open:
                    ##self.cursor.close()
                    self.connection.close()


    def extractDataProductsInfo(self,seller_id):  #Extraer datos de la Meli_Account X
       

        sql = f"""SELECT * FROM products_info_customers 
                  where seller_id={seller_id} and app_status = 1;"""

        again = 0
        while again == 0:

            try:
                self.cursor.execute(sql)
                #fetchall porque son varios resultados o todos
                #allData = list(self.cursor.fetchall())           
                #df = pd.DataFrame(allData, columns=["sku", "id_sku"])
                #df = pd.DataFrame(allData, columns=["sku", "sale_price","regular_price","stock_quantity", "max_weigth"])
                df = pd.read_sql(sql, self.connection)
                print("OK\n")
                #self.cursor.close()
                self.connection.close()
                return df

                
            except Exception as e:
                #raise
                again = 1
                print("Fallido: ", e)
                time.sleep(5) 
            finally:
                if self.connection.open:
                    #self.cursor.close()
                    self.connection.close()

    def extractUserData(self, seller_id):  #Extraer datos de la Meli_Account X
       

        sql = f"""SELECT * FROM parameters where seller_id={seller_id};"""

        again = 0
        while again == 0:

            try:
                #self.cursor.execute(sql)
                #fetchall porque son varios resultados o todos
                #allData = list(self.cursor.fetchall())           
                #df = pd.DataFrame(allData, columns=["sku", "id_sku"])
                #df = pd.DataFrame(allData, columns=["amazon_site", "meli_site_id","zip_code"])
                df = pd.read_sql(sql, self.connection) 
                print("OK\n")
                #self.cursor.close()
                self.connection.close()
                return df

                
            except Exception as e:
                #raise
                again = 1
                print("Fallido: ", e)
                time.sleep(5) 
            finally:
                if self.connection.open:
                    #self.cursor.close()
                    self.connection.close()

    def productsToUpdate(self,seller_id):  #Extraer datos de la Meli_Account X
       
        sql = f"""select * from products_info_customers where seller_id = {seller_id} and app_status = 1"""

        again = 0
        while again == 0:

            try:                
                df = pd.read_sql(sql, self.connection)
                again = 1
                return df
            except pymysql.Error as error:
                print(error)
                self.connection.rollback()
                print(f"Failed to make query")
            except NameError as error:
                print(error)
            finally:   
                if self.connection.open:
                    self.cursor.close()
                    self.connection.close()
                    print("MySQL connection is closed")
    
    
    def getSubscriptions(self,seller_id):  #Extraer datos de la Meli_Account X
       
        sql = f"""select * from subscriptions where seller_id = {seller_id} """

        again = 0
        while again == 0:

            try:                
                df = pd.read_sql(sql, self.connection)
                again = 1
                return df
            except pymysql.Error as error:
                print(error)
                self.connection.rollback()
                print(f"Failed to make query")
            except NameError as error:
                print(error)
            finally:   
                if self.connection.open:
                    self.cursor.close()
                    self.connection.close()
                    print("MySQL connection is closed")


    def getSchedule(self,seller_id):  #
       
        sql = f"""select * from update_schedule where seller_id = {seller_id} """

        again = 0
        while again == 0:

            try:                
                df = pd.read_sql(sql, self.connection)
                again = 1
                return df
            except pymysql.Error as error:
                print(error)
                self.connection.rollback()
                print(f"Failed to make query")
            except NameError as error:
                print(error)
            finally:   
                if self.connection.open:
                    self.cursor.close()
                    self.connection.close()
                    print("MySQL connection is closed")

    def getScheduleByDate(self,date_start,hour_start):  #
       
        sql = f"""select * from update_schedule where date_start = '{date_start}' and hour_start = '{hour_start}' """

        again = 0
        while again == 0:

            try:                
                df = pd.read_sql(sql, self.connection)
                again = 1
                return df
            except pymysql.Error as error:
                print(error)
                self.connection.rollback()
                print(f"Failed to make query")
            except NameError as error:
                print(error)
            finally:   
                if self.connection.open:
                    self.cursor.close()
                    self.connection.close()
                    print("MySQL connection is closed")



    def getIdSku(self, sku):
        
        sql = f"select id_sku from sku_products where sku = '{sku}';"
        try:
                self.cursor.execute(sql)
                item = self.cursor.fetchone()[0]                
                return item
        except Exception as e:
            print(e)
            return None
        finally:
            if self.connection.open:
                #self.cursor.close()
                self.connection.close()



    def updateBatch(self,table, id_init, id_last, **dict_to_update):
       

        sql = f"UPDATE {table} SET "
        keys = dict_to_update.keys()
        
        for key in keys:
            if type(dict_to_update[key]) != str:
                sql += f"{key} = {dict_to_update[key]}, "
            else:
                sql += f"{key} = '{dict_to_update[key]}', "
                
        sql = sql[:-2] 
            
        sql += f" WHERE id_sku BETWEEN {id_init} AND {id_last}"

        try:
            self.cursor.execute(sql)
            self.connection.commit() #Guarda Cambios
            #self.connection.close() #cerramosconexion <<<<
            #Persistencia del update, inset o delete
            print(f'\nupdated batch id_sku between {id_init} and {id_last}\n')
        except Exception as e:
            print(f'hubo un error en updateBatch: {e}')
            #raise  
        finally:
                if self.connection.open:
                    ##self.cursor.close()
                    self.connection.close()


    def getSkuProducts(self):
        sql = """select * from ecommerce.sku_products"""
        try:
            self.cursor.execute(sql)
            allData = list(self.cursor.fetchall())           
            #df = pd.DataFrame(allData, columns=["sku", "id_sku"])
            df = pd.DataFrame(allData, columns=["id_sku", "sku","id_category"])             
            return df
        except Exception as e:
            print(e)
        finally:
            if self.connection.open:
                #self.cursor.close()
                self.connection.close()


    def is_connected(self):
        return self.connection.open
    

    def reconnect(self):        
        return self.connection.ping(reconnect=True)


    def close(self):
        self.connection.close()


# # # if __name__ == '__main__':

# # #     #creo un objeto DataBase
# # #     database = DataLogManager()

# # #     sku = 'B004OODEUG'
# # #     country = 'Mexico'
# # #     available_quantity = 45
# # #     cop = 999999
# # #     last_updated = '2021-07-07 15:15:00'
# # #     maxWeigth = 0
# # #     item = list(database.selectItemBySku(sku))
# # #     print(f'item: {item}')
# # #     # [ids,skus,old_cop, old_available_quantity,
# # #     # old_last_updated,publishedDate,oldMaxWeigth] = database.extractAllDataByAccount(1)
# # #     # database.updateDataLog(sku,cop,available_quantity,last_updated,maxWeigth,country)

# # #     database.close()


## TABLA CREADA PARA dataLog * se definio sku como Primary_Key
# CREATE TABLE 'nymeliapp'.'dataLog' (
#   'id' VARCHAR(15) NOT NULL,
#   'sku' VARCHAR(15) NOT NULL,
#   'cop' INT NOT NULL,
#   'available_quantity' TINYINT(3) NOT NULL DEFAULT 0,
#   'last_updated' VARCHAR(40) NOT NULL,
#   'date_published' VARCHAR(40) NOT NULL,
#   'maxWeigth' MEDIUMINT(4) NULL DEFAULT 0,
#   'country' VARCHAR(40) NULL DEFAULT 0,
#   'meli_account' TINYINT(3) NOT NULL,
#   PRIMARY KEY ('id', 'sku'),
#   UNIQUE INDEX 'id_UNIQUE' ('id' ASC));   


if __name__ =="__main__":
    conn = DataLogManager("ecommerce")
    print("conectado? ",conn.is_connected())
    id = conn.getIdSku("B0979QLMYV")
    print(id)
    print("conectado? ",conn.is_connected())

    print("reconectando...")
    conn.reconnect()
    print("conectado? ",conn.is_connected())
    id = conn.getIdSku("B010G1VUMO")
    print(id)    