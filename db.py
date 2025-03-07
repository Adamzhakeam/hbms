'''
        the modules below are responsible for handling the database processes of the 
        business management system 
        pending features -cash drawer reconciliation 
                            ```
                                with this feature the user enters the cash in the register at 
                                the end of the day and compares with the expected amount,
                                total cash earned ,the money received  through cashless means,
                                is incremented ,the expenses are decremented , then deduct the 
                                cash started with at  the beginning of the day started with in the register 
                            ``` 
                        -mail smtp
                        -reports
                        -product discounts 
                        -refunds and returns of damaged goods
                        -invoices and other related documents 
                        -purchase order generation
                        -invoice generation
'''
import kisa_utils as kutils
import os
# ----- below is code to handle products-----
'''
    this is module is responsible for handling the insertion of information about 
    products and also fetching information of products and specific products 
'''
def insertProductIntoDb(product:dict)->dict:
    '''
        this function is responsible for inserting product into the database 
        @param product: 'productId','timestamp','userId','productName',productCategory,
                    'productCostPrice','productSalePrice','productQuantity','units',
                    'productSerialNumber','productImage','others','discount','discountExpiry'
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbtable = kutils.config.getValue('bmsDb/tables')
    discount = 0
    discountExpiry = 'yyyy-mm-dd'
    
    # productId,timestamp,userId,productName,productCategory,productCostPrice,productSalePrice,productQuantity,units,productSerialNumber,productImage,others = product.values()
    with kutils.db.Api(dbPath, dbtable, readonly=False ) as db:
        fetchProductByPertNumber = fetchSpecificProductByPn(product)
        fetchProductByCategory = fetchSpecificProductByCategory(product)
        if not fetchProductByPertNumber['status'] or not fetchProductByCategory['status']:
            
            productInsertionResponse = db.insert(
                'products',
                [product['productId'],product['timestamp'],product['userId'],product['productName'],product['productCategory'],product['productCostPrice'],
                product['productSalePrice'],product['productQuantity'],product['units'],product['productSerialNumber'],product['productImage'],product['others'],discount,discountExpiry]
                
            )
            return {'status':True,'log':productInsertionResponse}
        return{
            'status':False,
            'log':f'pert number already exists try updating product with this pert number -->{product["productSerialNumber"]} in the same category ==>{product["productCategory"]}'
        }
    
def editParticularProduct(productDetails:dict)->dict:
    ''''
        this module is responsible for edit a particular product
        @param  productDetails: these are the expected keys 'productName','productCategory','productCostPrice','productSalePrice',
        'productQuantity','units',productId 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    print('edit products ',productDetails)
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        productUpdateResponse = db.update('products',
                                          ['productName','productCategory','productCostPrice','productSalePrice','productQuantity','units'],
                                          [productDetails['productName'],productDetails['productCategory'],productDetails['productCostPrice'],
                                           productDetails['productSalePrice'],productDetails['productQuantity'],productDetails['units']],
                                          'productId = ?',[productDetails['productId']]
                                          )
        print(productUpdateResponse)
        return(productUpdateResponse)
    
def updateProductQuantity(productDetails:dict)->dict:
    '''
        this module is responsible for updating product quantity after making a sale 
        it returns a dictionary if with keys 'status' and 'log' if operation is successful it returns status as True and 
        if operation is not successful it returns False as status and the log contains the error 
        @param productDetails:->'productId' and 'Quantity' are the expected keys in the dictionary
     '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        quantityFetchResults = db.fetch('products',['productQuantity'],
                                        'productId = ?',[productDetails['productId']],
                                        limit = 1,
                                        returnDicts=True,
                                        returnNamespaces= False,
                                        parseJson= False,
                                        returnGenerator=False)
        currentQuantity = quantityFetchResults[0]['productQuantity']
        quantintyUpdateResponse = db.update('products',
                                            ['productQuantity'],
                                            [currentQuantity-productDetails['productQuantity']],
                                            'productId = ?',
                                            [productDetails['productId']])
        return(quantintyUpdateResponse)
    
    
    
def fetchSpecificProduct(productDetails:dict)->dict:
    '''
        this module is responsible for fetching for a specific product from the 
        database table products 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        productList = db.fetch(
            'products',
            ['productId','productName','productCategory','productCostPrice','productSalePrice','productSalePrice','productQuantity',
             'units','productSerialNumber','productImage'],
            'productName = ?',
            [productDetails['productName']],
            limit = 100,
            returnDicts= True,
            returnNamespaces= False,
            parseJson= False,
            returnGenerator= False
        )
    if not len(productList) :
        
            return {
                'status':False,
                'log':'No results Found'
            }
    return {'status':True,
                'log':productList
                }
def fetchSpecificProductById(productDetails:dict)->dict:
    '''
        this module is responsible for fetching for a specific product from the 
        database table products by Id 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        productList = db.fetch(
            'products',
            ['productId','productName','productCategory','productCostPrice','productSalePrice','productSalePrice','productQuantity',
             'units','productSerialNumber','others'],
            'productId = ?',
            [productDetails['productId']],
            limit = 1,
            returnDicts= True,
            returnNamespaces= False,
            parseJson= False,
            returnGenerator= False
        )
    if not len(productList) :
        
            return {
                'status':False,
                'log':'No results Found'
            }
    return {'status':True,
                'log':productList
                }
def fetchSpecificProductByPn(productDetails:dict)->dict:
    '''
        this module is responsible for fetching for a specific product from the 
        database table products by serial Number
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        productList = db.fetch(
            'products',
            ['productId','productName','productCategory','productCostPrice','productSalePrice','productSalePrice','productQuantity',
             'units','productSerialNumber','productImage'],
            'productSerialNumber = ?',
            [productDetails['productSerialNumber']],
            limit = 100,
            returnDicts= True,
            returnNamespaces= False,
            parseJson= False,
            returnGenerator= False
        )
    if not len(productList) :
        
            return {
                'status':False,
                'log':'No results Found'
            }
    return {'status':True,
                'log':productList
          
              }
    
def fetchSpecificProductByCategory(productDetails:dict)->dict:
    '''
        this module is responsible for fetching for a specific product from the 
        database table products by serial Number
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        productList = db.fetch(
            'products',
            ['productId','productName','productCategory','productCostPrice','productSalePrice','productSalePrice','productQuantity',
             'units','productSerialNumber','productImage'],
            'productCategory = ?',
            [productDetails['productCategory']],
            limit = 100,
            returnDicts= True,
            returnNamespaces= False,
            parseJson= False,
            returnGenerator= False
        )
    if not len(productList) :
            print(False)
        
            return {
                'status':False,
                'log':'No results Found'
            }
    print(True)
    return {'status':True,
                'log':productList
                }

def fetchAllProducts()->dict:
    '''
        this function is responsible for fetching all 
        the products from the database 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        productsList = db.fetch(
            'products',
            ['*'],
            '',
            [],
            limit = 100,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator=False
        )
    if not len(productsList) :
            return {
                'status':False,
                'log':"you haven`t registered any products yet"
            }
    return {
            'status':True,
            'log':productsList
        }

def fetchAllProductsWithWarningStock()->dict:
    '''
        this function is responsible for fetching all 
        the products from the database 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        productsList = db.fetch(
            'products',
            ['*'],
            'productQuantity <= ?',
            [5],
            limit = 100,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator=False
        )
    if not len(productsList) :
            return {
                'status':False,
                'log':"you dont have any products with warning stock as yet"
            }
    return {
            'status':True,
            'log':productsList
        }
    
def fetchAllProductsWithDiscount() -> dict:
    '''
    This function is responsible for fetching all products where
    the discount inside the `others` JSON column is greater than zero.
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        # Fetch all products and parse the JSON in the 'others' column
        productsList = db.fetch(
            'products',
            ['*'],  # Fetch all columns or specific ones if needed
            'discount > ?',  # No specific condition (fetch all products)
            [0],  # No condition data
            limit=100,  # Limit to 100 rows
            returnDicts=True,  # Return as a list of dictionaries
            returnNamespaces=False,
            parseJson=False,  # Parse JSON columns automatically
            returnGenerator=False
        )
        
        if not len(productsList):
            return {
                'status':False,
                'log':'You do not have any products with set discounts '
            }
        return {'status':True, 'log':productsList}
    

    
def createTables():
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTables = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath,dbTables, readonly=False) as db:
        creationResponse = db.createTables(dbTables)
        print('>>>>>>>>>>>>>>tables didnt exist')
    return creationResponse


# _______________the module below is responsible for handling SALES MODULE____
'''
        the module below is responsible for handling the creation of a sale and 
        inserting it into the database and fetching the sales accordingly 
'''
def addSaleToDB(sales: dict) -> dict:
    '''
        this function is responsible for adding the entire sale, 
        it returns a dictionary containing the status boolean and log string
        the log is empty incase everything is ok
        @param -> sales is an object containing the details of 
        a particular sale 
    '''
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    # entryId, saleId, timestamp, grandTotal, numberOfItemsSold, soldBy,soldTo,paymentType,paymentStatus,amountPaid, others = sales.values()

    with kutils.db.Api(dbPath, dbTable, readonly=False)as db:
        insertSaleStatus = db.insert(
            "sales", 
            [sales['entryId'], sales['saleId'], sales['timestamp'],sales['dateSold'], sales['grandTotal'], sales['numberOfItemsSold'], 
             sales['soldBy'],sales['soldTo'],sales['paymentType'], sales['paymentStatus'], sales['amountPaid'],sales['others']])
        return insertSaleStatus
    
def fetchSpecificSale(saleDetails:dict) -> dict:
    '''
        this function is responsible for fetching sales from database of a particular date
        @param date
    '''
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    date = saleDetails['saleDate']
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        specificSaleFetchResponse = db.fetch(
            'sales',
            ['*'],
            'dateSold = ?',[date],
            limit = 100,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
        return {
            'status':True,
            'log':specificSaleFetchResponse
        }

def fetchSpecificSaleById(saleDetails:dict) -> dict:
    '''
        this function is responsible for fetching sales from database of a particular date
        @param date
    '''
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    saleId = saleDetails['saleId']
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        specificSaleFetchResponse = db.fetch(
            'sales',
            ['*'],
            'saleId = ?',[saleId],
            limit = 1,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
        return {
            'status':True,
            'log':specificSaleFetchResponse
        }

    
def fetchSpecificSalesFromTo(saleDates:dict) -> dict:
    '''
        this function is responsible for fetching sales between a particular period of time 
        @ param saleDates:'dateFrom','dateTo' are the expected keys
    '''
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    dateFrom = saleDates['dateFrom']
    dateTo = saleDates['dateTo']
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        specificSaleFetchResponse = db.fetch(
            'sales',
            ['grandTotal','numberOfItemsSold','soldBy','soldTo','paymentType','paymentStatus','amountPaid'],
            'dateSold >= ? and dateSold <=?',[dateFrom,dateTo],
            limit = 100,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
        
        return {
            'status':True,
            'log':specificSaleFetchResponse
        }
    

    
def fetchAllSales()->dict:
    '''
    this function is responsible for fetching all the sales from the database
    it returns a list of the all the sales 
    '''
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    # print(dbPath)

    dbTable = kutils.config.getValue("bmsDb/tables")
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        salesFetchResponse = db.fetch(
            'sales',
            ['*'],
            '',[],
            limit = 100,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
        return {
            'status':True,
            'log':salesFetchResponse
        }

# ---- the code below handles report generation of sales ---
def fetch_sales_with_pagination(limit: int, page: int) -> dict:
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    
    offset = (page - 1) * limit
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        sales = db.fetch(
            'sales',
            ['*'],
            '',
            [],
            limit=limit,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator=False
        )[offset:offset + limit]  # Slice the result to simulate offset
        
        salesCount = db.fetch(
            'sales',['*'],'',[],limit=6000,returnDicts=True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        
        totalCount = len(salesCount)
        
        return {
            'status': True,
            'log': sales,
            'total':totalCount
        }
        
def fetchSpecificSaleReport(limit:int,page:int,saleDetails:dict) -> list:
    '''
        this function is responsible for fetching sales from database of a particular date
        @param date,limit,int
    '''
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    date = saleDetails['saleDate']
    
    offset = (page - 1) * limit
    
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        specificSaleFetchResponse = db.fetch(
            'sales',
            ['*'],
            'dateSold = ?',[date],
            limit = limit,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )[offset:offset + limit] 
        
        fetchResponse =  db.fetch(
            'sales',
            ['*'],
            'dateSold = ?',[date],
            limit = 6000,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
        totalCount = len(fetchResponse)
        
        return {
            'status': True,
            'log': specificSaleFetchResponse,
            'total':totalCount
        }
        
def fetchSpecificSalesFromToReports(limit:int,page:int,saleDates:dict) -> list:
    '''
        this function is responsible for fetching sales between a particular period of time 
        @ param saleDates:'dateFrom','dateTo' are the expected keys
    '''
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    dateFrom = saleDates['dateFrom']
    dateTo = saleDates['dateTo']
    offset = (page - 1) * limit
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        specificSaleFetchResponse = db.fetch(
            'sales',
            ['grandTotal','numberOfItemsSold','soldBy','soldTo','paymentType','paymentStatus','amountPaid'],
            'dateSold >= ? and dateSold <=?',[dateFrom,dateTo],
            limit = limit,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )[offset:offset + limit] 
        
        fetchResponse = db.fetch(
            'sales',
            ['grandTotal','numberOfItemsSold','soldBy','soldTo','paymentType','paymentStatus','amountPaid'],
            'dateSold >= ? and dateSold <=?',[dateFrom,dateTo],
            limit = 6000,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
        
        totalCount = len(fetchResponse)
        
        return {
            'status': True,
            'log': specificSaleFetchResponse,
            'total':totalCount
        }


    
# def addSingleProductSale(singleProductSales: list) -> dict:
#     '''
#         this function is responsible for adding the 
#         individual goods of a particular sale into the table 
#         it returns a dictionary containing the status boolean and log string
#         the log is empty incase everything is ok

#         @param -> singleProductSale is an object containing the details 
#         of the individual product(details)
#     '''
#     dbPath = kutils.config.getValue("bmsDb/dbPath")
#     dbTable = kutils.config.getValue("bmsDb/tables")
#     singleProductSale = {}
    
#     for productSale in range(len(singleProductSales)):
#         # print(singleProductSales[productSale]['entryId'])
    
#         entryId, timestamp, saleId, productId, unitPrice, units,quantity, total, others = singleProductSales[productSale].values()
    

#         with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
#             insertStatus = db.insert(
#                 "productSales",
#                 [entryId, timestamp, saleId, productId, unitPrice, units,quantity, total, others])
#     return insertStatus

def addSingleProductSale(singleProductSales: list) -> dict:
    """
    This function is responsible for adding the 
    individual goods of a particular sale into the table. 
    It returns a dictionary containing the status boolean and log string.
    The log is empty if everything is OK.

    @param -> singleProductSales is a list of objects containing the details 
    of the individual products.
    """
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    
    status = True
    log = ""

    for productSale in singleProductSales:
        # try:
            # entryId, timestamp, saleId, productId, unitPrice, units, quantity, total,others = productSale.values()

            with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
                insertStatus = db.insert(
                    "productSales",
                    [productSale['entryId'], productSale['timestamp'], productSale['dateSold'],productSale['saleId'], productSale['productId'], 
                     productSale['unitPrice'], productSale['productQuantity'], productSale['units'], productSale['total'], productSale['others']]
                )
                response = updateProductQuantity(productSale)
                print('productSubResp',response) 
                
                if not insertStatus['status']:
                    status = False
                    log += f"Failed to insert product sale: {productSale}\n"
                    return {'status':status, 'log':log}
        
        # # except Exception as e:
        #     status = False
        #         log += f"Error processing product sale {productSale}: {e}\n"
        #     return {'status':status, 'log':log}
        # print(updateProductQuantity(productSale))

    return {"status": status, "log": log}

# --#-- the modules below are responsible for handling users----- #---#--#--#-

def createuser(userDetails:dict)->dict:
    '''
        this module is responsible for creation of a user 
        @param userDetails:'userName','password',
                            'phoneNumber','roleId','email' are the expected keys 
        returns a dictionary with status and log 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    passwordHash = kutils.encryption.hash(userDetails['password'])
    entryId = kutils.codes.new()
    timestamp = kutils.dates.currentTimestamp()
    userId = kutils.codes.new()
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        phoneNumberResponse = db.fetch(
            'users',
            ['phoneNumber'],
            'phoneNumber = ?',
            [userDetails['phoneNumber']],
            limit = 1,
            returnDicts=True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
        if len(phoneNumberResponse) > 0:
            return{'status':False, 'log':'phoneNumber already exists attached to another user please try another'}
        userCreationResponse = db.insert(
            'users',
            [entryId,timestamp,userId,userDetails['userName'],
             passwordHash,userDetails['phoneNumber'],userDetails['email'],userDetails['roleId']]
        )
    return(userCreationResponse)

def fetchAllusers()->list:
    '''
        this function is responsible for fetching customer from db
        by use of phone number
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        customerFetchResponse = db.fetch(
            'users',
            ['*'],
            '',
            [],limit = 100,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        if len(customerFetchResponse) == 0:
            return {
                'status':False,
                'log':'you havent registered any users yet'
            }
        return {
            'status':True,
            'log':customerFetchResponse
        }
def fetchuserByPhoneNumber(userDetails:dict)->dict:
    '''
    this module is responsible for fetching user by phone number
    @param userDetails:expected keys 'phoneNumber'
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        userFetchResponse = db.fetch(
            'users',['*'],'phoneNumber=?',[userDetails['phoneNumber']],
            limit = 1 ,returnDicts= True,
            returnNamespaces=False,parseJson=False,returnGenerator=False
        )  
        if  len(userFetchResponse) == 0 :
            return {
                'status':False,
                'log':f'No users found registered under {userDetails["phoneNumber"]}'
            } 
        return{
            'status':True,
            'log':userFetchResponse
        }

def insertRevokeduser(userDetails:dict) -> dict:
    '''
        this module is responsible for inserting a revoked user into db 
        @param userDetails:entryId, timestamp, userId,userName,password ,phoneNumber, email,roleId,other the following 
                            are the expected keys
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly = False) as db:
        entryId = kutils.codes.new()
        timestamp = kutils.dates.currentTimestamp()
        if userDetails['other']['revokerId'] == userDetails['userId']:
            return{
                'status':False,
                'log':'user can`t revoke themselves'
            }
        revokeduserInsertionResponse = db.insert( 'revokeduser',
                                                 [entryId,timestamp,userDetails['userId'],userDetails['userName'],
                                                      userDetails['password'],userDetails['phoneNumber'],userDetails['email'],
                                                      userDetails['roleId'],userDetails['other']])
        return revokeduserInsertionResponse   
    
def resetuserPassword(userDetails:dict)->dict:
    '''
        this function is responsible for resetting users password
        @param userDetails: 'phoneNumber' is the expected key  
    ''' 
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    newPassword = kutils.codes.new(8)
    passwordHash = kutils.encryption.hash(newPassword)
    if fetchuserByPhoneNumber({'phoneNumber':userDetails['phoneNumber']})['status']:
        email = fetchuserByPhoneNumber({'phoneNumber':userDetails['phoneNumber']})['log'][0]['email']
        with kutils.db.Api(dbPath,dbTable,readonly=False) as db:
            passwordUpdateResponse = db.update('users',
                                               ['password'],[passwordHash],'phoneNumber = ?',
                                               [userDetails['phoneNumber']])
            if passwordUpdateResponse['status']:
                return{'status':True,'log':f"your new password is: {newPassword}",'email':email}
            return passwordUpdateResponse
    return {'status':False,'log':'There is no user registered under the phoneNumber provided '}

def login(userDetails:dict)->dict:
    '''
        this function is responsible for verifying credentials from the front end 
        @param userDetails:'phoneNumber','email','password' are the expected keys  
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    passwordHash = kutils.encryption.hash(userDetails['password'])
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        userFetchResponse = db.fetch(
            'users',
            ['userId','userName','phoneNumber','password','roleId'],'phoneNumber=? or email=? and password=? ',
            [userDetails['phoneNumber'],userDetails['email'],passwordHash],
            limit = 1,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator=False
        )
        if len(userFetchResponse) > 0:
            return {'status':True, 'log':userFetchResponse}
        return{'status':False, 'log':'You have input a wrong password or email/phoneNumber'}
    
# -- this module responsible for creating roles 
def createRoles(roleDetails:dict)->dict:
    '''
        this module is responsible for creation of roles and adding them to the db
        @param roleDetails:'entryId','timestamp','roleId','role','others'
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    entryId = kutils.codes.new()
    roleId = kutils.codes.new()
    timestamp = kutils.dates.currentTimestamp()
    role = roleDetails['role'].upper()
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        roleInsertionResponse = db.insert(
            'roles',
            [entryId,timestamp,roleId,role,roleDetails['others']]
        )
        return roleInsertionResponse
    
def fetchRole(roleDetails:dict)->list:
    '''
        this function is responsible for fetching the user role 
        from database 
        @param roleId:
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        roleFetchResults = db.fetch(
            'roles',
            ['role'],
            'roleId = ?',
            [roleDetails['roleId']],
            limit = 1,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator= False
        )
        if len(roleFetchResults) == 0:
            return{
                'status':False,
                'log':"role does not exist"
            }
        
        return {
            'status':True,
            'log':roleFetchResults
        }
    
    
def fetchAllRoles()->list:
    '''
        this function is responsible for fetching the user role 
        from database 
        @param roleId:
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        roleFetchResults = db.fetch(
            'roles',
            ['*'],
            '',
            [],
            limit = 100,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator= False
        )
        if len(roleFetchResults) == 0:
            return{
                'status':False,
                'log':"you haven`t registered any roles yet"
            }
        return{
            'status':True,
            'log':roleFetchResults
        }

# --- this module is responsible for handling 
def createUnit(unitDetails:dict)->dict:
    '''
        this module is responsible for creation of roles and adding them to the db
        @param roleDetails:'entryId','timestamp','roleId','role','others'
    '''
    # import pprint
    # print('>>>>>>>fromFrontend createUnit',unitDetails)
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    entryId = kutils.codes.new()
    timestamp = kutils.dates.currentTimestamp()
    unitId = kutils.codes.new()
    unit = unitDetails['unit'].upper()
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        roleInsertionResponse = db.insert(
            'units',
            [entryId,timestamp,unitId,unit,unitDetails['others']]
        )
        return roleInsertionResponse
    
def fetchUnit(unitDetails:dict)->list:
    '''
        this function is responsible for fetching the user role 
        from database 
        @param roleId:
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        roleFetchResults = db.fetch(
            'units',
            ['unit'],
            'unitId = ?',
            [unitDetails['unitId']],
            limit = 1,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator= False
        )
        if len(roleFetchResults) == 0:
            return{
                'status':False,
                'log':"unit does not exist"
            }
        print(roleFetchResults)
        return {
            'status':True,
            'log':roleFetchResults
        }
    
    
def fetchAllUnits()->list:
    '''
        this function is responsible for fetching the user role 
        from database 
        @param roleId:
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        roleFetchResults = db.fetch(
            'units',
            ['*'],
            '',
            [],
            limit = 100,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator= False
        )
        if len(roleFetchResults) == 0:
            return{
                'status':False,
                'log':"you haven`t registered any units yet"
            }
        return{
            'status':True,
            'log':roleFetchResults
        }

 
# ---the modules below are responsible for handling customers
'''
    this module is responsible for handling customers adding them to the database and 
    fetching their information from there database
'''
def addCustomerToDb(customerDetails:dict)->dict:
    '''
        this function inserts customer into database 
        @param customerDetails:'entryId','timestamp','customerId',customerName',
                                'customerPhoneNumber','customerLocation','others'
                                are the expected keys
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
         customerFetchResponse = db.fetch(
            'customers',
            ['customerPhoneNumber'],
            'customerPhoneNumber = ?',
            [customerDetails['customerPhoneNumber']],limit = 1,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
         if len(customerFetchResponse) > 0:
             return{'status':False, 'log':f'customer already registered using this {customerDetails["customerPhoneNumber"]}'}
            
         customerInsertionResponse = db.insert(
            'customers',
            [customerDetails['entryId'],customerDetails['timestamp'],customerDetails['customerId'],
             customerDetails['customerName'],customerDetails['customerPhoneNumber'],customerDetails['customerLocation'],customerDetails['others']]
        )
         return customerInsertionResponse
    
def fetchCustomer(phoneNumber:int)->list:
    '''
        this function is responsible for fetching customer from db
        by use of phone number
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        customerFetchResponse = db.fetch(
            'customers',
            ['*'],
            'customerPhoneNumber = ?',
            [phoneNumber],limit = 1,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        if len(customerFetchResponse) == 0:
            return{
                'status':False,
                'log':f"there is no customer registered under this{phoneNumber}"
            }
        return{
            'status':True,
            'log':customerFetchResponse
        }
    
    
def fetchCustomerById(customerDetails:dict)->list:
    '''
        this function is responsible for fetching customer from db
        by use of customerId
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        customerFetchResponse = db.fetch(
            'customers',
            ['*'],
            'customerId = ?',
            [customerDetails['customerId']],limit = 1,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        return customerFetchResponse
def fetchAllCustomers()->dict:
    '''
        this function is responsible for fetching customer from db
        by use of customerId
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        customerFetchResponse = db.fetch(
            'customers',
            ['*'],
            '',
            [],limit = 100,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        if len(customerFetchResponse) == 0:
            return{
                'status':False,
                'log':'you haven`t registered any customers yet'
                }
        return {
            'status':True,
            'log':customerFetchResponse
        }
    


# ----the module below handles product categories----
'''
    this module is responsible for adding and fetching 
    product categories to and from the database 
'''
def addCategoryToDb(categoryDetails:dict)->dict:
    '''
        this function is responsible for adding category to Db
        @param categoryDetails:'category',others are the expected keys
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    entryId = kutils.codes.new()
    timestamp = kutils.dates.currentTimestamp()
    categoryId = 'categoryId'+kutils.codes.new()
    # category = 
    categoryName = categoryDetails['category'].upper()
    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
        categoryFetchResponse = db.fetch(
            'categories',
            ['category'],
            'category = ?',
            [categoryName],limit = 1,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        if len(categoryFetchResponse) > 0:
            return{'status':False, 'log':f'{categoryName} has already been registered'}
    

        categoryInsertionResponse = db.insert(
            'categories',
            [entryId,timestamp,categoryId,
             categoryName,categoryDetails['others']]
        )
    return categoryInsertionResponse

def fetchCategory(categoryName:str)->list:
    '''
        this function is responsible for adding category to Db
        @param categoryName
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
         categoryFetchResponse = db.fetch(
            'categories',
            ['category'],
            'category = ?',
            [categoryName],limit = 1,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
         if len(categoryFetchResponse) == 0:
             return{
                 'status':False,
                 'log':f"there is no category regestered under the name{categoryName}"
             }
    return{
        'status':True,
        'log':categoryFetchResponse
    } 


def fetchAllCategories()->list:
    '''
        this function is responsible for adding category to Db
        @param categoryName
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
         categoryFetchResponse = db.fetch(
            'categories',
            ['*'],
            '',
            [],limit = 100,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
         if len(categoryFetchResponse) == 0:
             {
                 'status':False,
                 'log':"you haven`t registered anything yet"
             }
    return {
        'status':True,
        'log': categoryFetchResponse
    } 


# ---the module below is responsible for handling credit and debtors ---
'''
    this module is responsible for adding and fetching creditors 
    according to the sale information
'''
def addCreditDetailsToDb(creditDetails:dict)->dict:
    '''
        this function is responsible for adding credit details to the db
        @param creditDetails:'saleId','soldTo','amountInDebt','paymentStatus',others
                            are the expected keys
    '''
    
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    entryId = 'entryId'+kutils.codes.new()
    timestamp = kutils.dates.currentTimestamp()
    creditId = 'creditId'+kutils.codes.new()
    print('dtls',creditDetails)
    print(entryId,timestamp,creditId)
    amountInDebt = creditDetails['grandTotal'] - creditDetails['amountPaid']
    print('amountindebt',amountInDebt)
    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
        if creditDetails['paymentStatus'] == 'partialPayment':
            creditInsertionResponse = db.insert(
                'credits',
                [entryId,timestamp,creditId,creditDetails['saleId'],creditDetails['soldBy'],creditDetails['soldTo'],
                 amountInDebt,creditDetails['paymentStatus'],creditDetails['others']]
            )
            return creditInsertionResponse
        return {'status':False,'log':''}
    
def editCredit(creditDetails:dict)->dict:
    '''
        this module is responsible for editing the credit status of a customer 
        this i function does not obey the rules of functions am tired
        @param creditDetails:'creditId','saleId','amountInDebt','amountPaid','paymentStatus' are the expected keys 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTables = kutils.config.getValue('bmsDb/tables')
    idFetchResponse = fetchAllCreditById(creditDetails['creditId'])
    currentAmountInDebt = idFetchResponse['log'][0]['amountInDebts']
    print('CAIND',currentAmountInDebt)
    currentDebt = currentAmountInDebt - creditDetails['amountPaid']
    with kutils.db.Api(dbPath,dbTables, readonly = False) as db:
        if currentDebt  == 0:
            creditDetails['paymentStatus'] = 'Cleared'
            
            creditUpdateResponse = db.update(
                    'credits',
                    ['amountInDebts','paymentStatus'],
                    [currentDebt,creditDetails['paymentStatus']],
                    'creditId = ?',[creditDetails['creditId']]
                    
                )
            if creditUpdateResponse['status'] and currentDebt == 0:
                    saleUpdateResponse = editSale({'saleId':creditDetails['saleId'],'paymentStatus':creditDetails['paymentStatus'],'amountPaid':creditDetails['amountPaid']})
                    return saleUpdateResponse
            return {
                'status':True,
                'log':'successfully updated'
            }
        creditUpdateResponse = db.update(
                    'credits',
                    ['amountInDebts','paymentStatus'],
                    [currentDebt,creditDetails['paymentStatus']],
                    'creditId = ?',[creditDetails['creditId']]
                    
                )
    if creditUpdateResponse['status'] :
                    saleUpdateResponse = editSale({'saleId':creditDetails['saleId'],'paymentStatus':creditDetails['paymentStatus'],'amountPaid':creditDetails['amountPaid']})
                    return saleUpdateResponse
    return {
                'status':True,
                'log':'successfully updated'
            }

def fetchAllCredits():
    '''
        this function is responsible for fetching product sales details 
        from table product sales 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
         creditsFetchResponse = db.fetch(
            'credits',
            ['*'],
            '',
            [],limit = 100,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
         if len(creditsFetchResponse) == 0:
             return{
                 'status':False,
                 'log':'You have not made any sales yet'
             }
         return {
             'status':True,
             'log':creditsFetchResponse
        
        }
         
def fetchAllUnClearedCredits():
    '''
        this function is responsible for fetching uncleared  debtors details 
        from table credits 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
         creditsFetchResponse = db.fetch(
            'credits',
            ['*'],
            'amountInDebts > ?',
            [0],limit = 100,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
         if len(creditsFetchResponse) == 0:
             return{
                 'status':False,
                 'log':'You have not made any sales yet'
             }
         return {
             'status':True,
             'log':creditsFetchResponse
        
        }


def fetchAllCreditById(creditId:str)->dict:
    '''
        this function is responsible for fetching product sales details 
        from table product sales 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
         creditsFetchResponse = db.fetch(
            'credits',
            ['amountInDebts'],
            'creditId = ?',
            [creditId],limit = 1,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
         if len(creditsFetchResponse) == 0:
             return{
                 'status':False,
                 'log':'You have not made any sales yet'
             }
         print('yes')
         return {
             'status':True,
             'log':creditsFetchResponse
        
        }

    
        
    # -----the module below is responsible for fetching all the sales of a particular product ----
def fetchAllProductSales():
    '''
        this function is responsible for fetching product sales details 
        from table product sales 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
         productSalesFetchResponse = db.fetch(
            'productSales',
            ['*'],
            '',
            [],limit = 100,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
         if len(productSalesFetchResponse) == 0:
             return{
                 'status':False,
                 'log':'You have not any products sold yet'
             }
         return {
             'status':True,
             'log':productSalesFetchResponse
        
        }
         
def fetchSpecificProductSale(saleDetails:dict) -> list:
    '''
        this function is responsible for fetching sales from database of a particular date
        @param date
    '''
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    date = saleDetails['saleDate']
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        specificProductSaleFetchResponse = db.fetch(
            'productSales',
            ['*'],
            'dateSold = ?',[date],
            limit = 100,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
    if len(specificProductSaleFetchResponse) == 0:
        return{
            'status':False,
            'log':f'there were no Products Sold on this day {date} '
        }
    return {
        'status':True,
        'log':specificProductSaleFetchResponse
    }
    
def fetchSpecificProductSalesFromTo(saleDates:dict) -> list:
    '''
        this function is responsible for fetching sales between a particular period of time 
        @ param saleDates:'dateFrom','dateTo' are the expected keys
    '''
    dbPath = kutils.config.getValue("bmsDb/dbPath")
    dbTable = kutils.config.getValue("bmsDb/tables")
    dateFrom = saleDates['dateFrom']
    dateTo = saleDates['dateTo']
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        specificProductSaleFetchResponse = db.fetch(
            'productSales',
            ['*'],
            'dateSold >= ? and dateSold <=?',[dateFrom,dateTo],
            limit = 100,
            returnDicts= True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
    if not len(specificProductSaleFetchResponse):
        return{
            'status':False,
            'log':f'You didn`t make any sales in the dates selected {dateFrom} to {dateTo} '
        }
        
    return {
            'status':True,
            'log':specificProductSaleFetchResponse
        }
    
def editSale(saleDetails:dict)->dict:
    '''
        this function is responsible for updating a specific sale 
        by the sale Id 
        @param saleDetails: 'saleId','paymentStatus' are the expected keys
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    amountPaidFetch = fetchSpecificSaleById(saleDetails)
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        salesUpdateResponse = db.update(
            'sales',
            ['paymentStatus','amountPaid'],
            [saleDetails['paymentStatus'],amountPaidFetch['log'][0]['amountPaid']+saleDetails['amountPaid']],
            'saleId = ?',
            [saleDetails['saleId']]
        )
        print(salesUpdateResponse)
        return salesUpdateResponse

        
# ------the modules below are responsible for handling expenses 
'''
    the functions below are responsible for handling expenses ,
    inserting ,updating and fetching 
'''
def addExpenseToDb(expenseDetails:dict)->dict:
    '''
        this function handles insertion of expenses into the database 
        @param: expected keys in the dictionary 'entryId','timestamp','dateOfExpense','description','amountSpent','others'
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        expenseInsertionResponse = db.insert(
            'expenses',
            [expenseDetails['entryId'],expenseDetails['timestamp'],expenseDetails['dateOfExpense'],
             expenseDetails['description'],expenseDetails['amountSpent'],expenseDetails['others']
             ]
        )
    return expenseInsertionResponse
    
def fetchExpensesFromDb()->dict:
    '''
        this function is responsible for fetching all expenses from the database 
    '''    
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        expenseFetchResponse = db.fetch(
            'expenses',
            ['*'],
            condition = '',
            conditionData = [],
            limit = 100,
            returnDicts= True,
            returnNamespaces = False ,
            parseJson= False,
            returnGenerator= False
        )
        
    if not len(expenseFetchResponse):
            return{'status':False,'log':"you haven`t registered any expenses yet "}
    return {
        'status':True,
        'log':expenseFetchResponse
    }
    
def fetchSpecificExpenseByDate(expenseDetails:dict)->dict:
    '''
        the following function is responsible if fetching a specific expense from database
        that was made on  specific date 
        @param:expenseDetails 'dateOfExpense'
        
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        expenseFetchResponse = db.fetch(
            'expenses',['*'],'dateOfExpense = ?',
            [expenseDetails['dateOfExpense']], limit = 100, returnDicts= True,
            returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        if not len(expenseFetchResponse):
            return{
                'status':False,
                'log':"You dont have any expenses on this date"
            }
        return {
            'status':True,
            'log':expenseFetchResponse
        }
        
def fetchSpecificExpensesFromTo(dateDetails:dict)->dict:
    '''
        this function is responsible for fetching expenses from and to a specific  date
        @param dateDetails:'dateFrom','dateTo' are the expected keys 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    dateFrom = dateDetails['dateFrom'],
    dateTo = dateDetails['dateTo']
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        expenseFetchResponse = db.fetch(
            'expenses',['*'],'dateOfExpense >= ? and dateOfExpense <= ?',
            [dateFrom,dateTo],limit=100,returnDicts=True,returnNamespaces=False,
            parseJson=False,returnGenerator=False
        )
        if not len(expenseFetchResponse):
            return{
                'status':False,
                'log':f'you dont have any sales between {dateFrom} and {dateTo} '
            }
        return {
            'status':True,
            'log':expenseFetchResponse
        }
        
#-------the modules below are for removing a user from database----

def removeuserFromDb(userDetails:dict)->dict:
    '''
        this function deletes user from database table users
        @param: expected key is 'phoneNumber'
    '''
    dbPath= kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
       
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
            userDeleteResponse = db.delete(
                'users',
                'phoneNumber = ?',
                [userDetails['phoneNumber']]
            ) 
    return userDeleteResponse

def revokeuser(userDetails:dict)->dict:
    '''
    this function is responsible for revoking user
    @param userDetails: the expected keys are 'phoneNumber','other' 
    '''
    userToRevoke = fetchuserByPhoneNumber(userDetails)
    if userToRevoke['status']:
        userToRevoke['log'][0]['other'] = userDetails['other']
        # print('>>>',userToRevoke['log'][0])
        transferuserResponse = insertRevokeduser(userToRevoke['log'][0])
        if transferuserResponse['status']:
           userDropResponse  = removeuserFromDb(userDetails)
           if userDropResponse['status']:
               return {'status':True,'log':f"user {userToRevoke['log'][0]['userName'] } revoked successfully"}
           return userDropResponse
        return transferuserResponse 
    return userToRevoke

# --- the modules below are responsible for handling discounts 
def calculateDiscount(discountDetails:dict)->dict:
    '''
    this function is responsible for calculating discount of 
    product(s) 
    @param discountDetails:the expected keys are 'discountRate' ,'productSalePrice
    the value for discountRate is  string which is either a percentage or
    a discount price  
    '''
    if discountDetails['discountRate'].endswith('%'):
        newPx = int(discountDetails['discountRate'].strip('%'))
        discountPrice = (newPx)*0.01
        return{'discount':discountPrice}
    else:
        discountPrice = int(discountDetails['discountRate'])
        return{'discount':discountPrice}



def setProductFlatDiscountPrice(discountingDetails: dict) -> dict:
    '''
    This function is responsible for setting the discount price 
    to the specific product(s) that have been selected.
    
    @param discountingDetails: the expected keys are 'discountRate',
                               'productIds', and 'discountExpiry'
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    discountExpiry = kutils.dates.today()
    
    
    # Initialize lists to collect update responses and errors
    updateResponses = []
    errors = []
    
    for productId in discountingDetails['productIds']:
        productFetchResponse = fetchSpecificProductById({'productId': productId})
        
        if productFetchResponse['status']:
            productDetails = productFetchResponse['log'][0]
            
            try:
                # Calculate the discount using the calculateDiscount function
                discount = calculateDiscount(discountingDetails)['discount']
                
                # Check if the discount is greater than the product sale price
                if discount >= productDetails['productSalePrice']:
                    errors.append({'productId': productId, 'error': 'Discount exceeds product sale price'})
                    continue  # Skip this product if the discount is greater or equal to the sale price
                
                # Calculate the discounted price
                discountedPrice = productDetails['productSalePrice'] - discount
                
                # Update the product in the database
                with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
                    updateResponse = db.update(
                        'products',
                        ['discount','discountExpiry'],
                        [discountedPrice,discountExpiry],
                        'productId=?', 
                        [productId]
                    )
                    
                    # Add the successful update response to the list
                    if updateResponse['status']:
                        updateResponses.append(productDetails['productName'])
                    else:
                        # Add to errors if the update failed
                        errors.append({'productId': productId, 'error': 'Update failed'})
            
            except Exception as e:
                # Catch any exceptions and add them to the errors list
                errors.append({'productId': productId, 'error': str(e)})
        
        else:
            # Add to errors if the product fetch failed
            errors.append({'productId': productId, 'error': 'Product not found'})
    
    # Return both successful updates and any errors encountered
    print('running1')
    return {
        'status': False if errors else True,
        'updatedProducts': updateResponses,
        'errors': errors
    }

def setProductDiscountPrice(discountingDetails: dict) -> dict:
    '''
    This function is responsible for setting the discount price 
    to the specific product(s) that have been selected.
    
    @param discountingDetails: the expected keys are 'discountRate',
                               'productIds', and 'discountExpiry'
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    discountExpiry = kutils.dates.today()
    
    
    # Initialize lists to collect update responses and errors
    updateResponses = []
    errors = []
    
    for productId in discountingDetails['productIds']:
        productFetchResponse = fetchSpecificProductById({'productId': productId})
        
        if productFetchResponse['status']:
            productDetails = productFetchResponse['log'][0]
            
            try:
                # Calculate the discount using the calculateDiscount function
                newPx = calculateDiscount(discountingDetails)['discount']
                discount = productDetails['productSalePrice']*newPx
                
                # Check if the discount is greater than the product sale price
                if discount >= productDetails['productSalePrice']:
                    errors.append({'productId': productId, 'error': 'Discount exceeds product sale price'})
                    continue  # Skip this product if the discount is greater or equal to the sale price
                
                # Calculate the discounted price
                discountedPrice = productDetails['productSalePrice'] - discount
                
                # Update the product in the database
                with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
                    updateResponse = db.update(
                        'products',
                        ['discount','discountExpiry'],
                        [discountedPrice,discountExpiry],
                        'productId=?', 
                        [productId]
                    )
                    
                    # Add the successful update response to the list
                    if updateResponse['status']:
                        updateResponses.append(productDetails['productName'])
                    else:
                        # Add to errors if the update failed
                        errors.append({'productId': productId, 'error': 'Update failed'})
            
            except Exception as e:
                # Catch any exceptions and add them to the errors list
                errors.append({'productId': productId, 'error': str(e)})
        
        else:
            # Add to errors if the product fetch failed
            errors.append({'productId': productId, 'error': 'Product not found'})
    
    # Return both successful updates and any errors encountered
    return {
        'status': False if errors else True,
        'updatedProducts': updateResponses,
        'errors': errors
    }

def resetProductDiscountDetails() -> dict:
    '''
    This function is responsible for resetting the discount details for 
    products with discounts on their expiry date.
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    today = kutils.dates.today()  # Get the current date in 'yyyy-mm-dd' format
    
    updatedProducts = []  # List to hold names of updated products
    
    if fetchAllProductsWithDiscount()['status']:
        discountedProductList = fetchAllProductsWithDiscount()['log']
        
        for product in discountedProductList:
            try:
                # Check if the product's discountExpiry matches today's date
                if product['discountExpiry'] == today:
                    # Open database connection in read-write mode to update the product
                    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
                        response = db.update(
                            'products',  # Table name
                            ['discount', 'discountExpiry'],  # Columns to update
                            [0, '0000-00-00'],  # Set discount to 0 and expiry to default
                            'productId = ?',  # Condition for update
                            [product['productId']]  # Condition data
                        )
                    
                    # If the update was successful, append the product name to updatedProducts list
                    if response['status']:  # Assuming response is a dictionary with a 'status' key
                        updatedProducts.append(product['productName'])
            except Exception as e:
                # Log error (optional, depending on how you handle errors in your library)
                print(f"Error updating product {product['productId']}: {str(e)}")
                continue  # Continue to the next product even if there's an error
        
        # Join the updated products into a single string, separated by commas
        updatedProductsStr = ', '.join(updatedProducts)
        
        # Return the result
        if updatedProductsStr:
            print('running2')
            return {
                'status': True,
                'updatedProducts': updatedProductsStr
            }
    print('running1')   
    return {
        'status': False,
        'log': "No products had discounts expiring today."
    }



# def SetProductDiscountPrice(discountingDetails: dict) -> dict:
#     '''
#     Optimized method to set discount prices for a batch of products using threading.
    
#     @param discountingDetails: The expected keys are 'discountRate', 'productIds', and 'expiryDate'
#                                - 'productIds' is a list of product IDs to update
#                                - 'discountRate' is the discount to apply (can be percentage or fixed)
    
#     This method batches product updates into concurrent threads to process them efficiently.
#     '''
#     dbPath = kutils.config.getValue('bmsDb/dbPath')
#     dbTable = kutils.config.getValue('bmsDb/tables')
    
#     updateResponses = []
#     errors = []
    
#     def processProduct(productId:str):
#         '''
#         Inner function to process each product's discount.
#         '''
#         productFetchResponse = fetchSpecificProductById({'productId': productId})
        
#         if productFetchResponse['status']:
#             try:
#                 discountingDetails['productSalePrice'] = productFetchResponse['log'][0]['productSalePrice']
#                 discount = calculateDiscount(discountingDetails)['discount']
#                 print('>>>>>>>>',discount)
#                 # Calculate the discounted price
#                 discountedPrice = productFetchResponse['log'][0]['productSalePrice'] - discount
                
#                 with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
#                     updateResponse = db.update(
#                         'products',
#                         ['others'],
#                         [{'omega': discountedPrice}],
#                         'productId=?', 
#                         [productId]
#                     )
                    
#                     if updateResponse['status']:
#                         updateResponses.append(productFetchResponse['log'][0]['productName'])
#                     else:
#                         errors.append(productId)
#             except Exception as e:
#                 errors.append({'productId': productId, 'error': str(e)})
#         else:
#             errors.append({'productId': productId, 'error': 'Product not found'})
    
#     # Use threading to handle multiple products at once
#     for productId in discountingDetails['productIds']:
#         kutils.threads.runOnce(processProduct, productId)
    
#     # Wait for all threads to complete and gather results
#     return {
#         'status': False if errors else True,
#         'updatedProducts': updateResponses,
#         'errors': errors
#     }

def setFlatSaleDiscount(discountDetails:dict)->dict:
    '''
        this function is responsible for 'handling 
        flatSale discount  and setting the discounted price 
        @param discountDetails: 'discountRate','weightAmount',amountPaid
    '''
    discount = calculateDiscount(discountDetails)
    print(">>>>>>>>>>>>>>>>>topnotchdebugger", discountDetails['amountPaid'],discount['discount'])
    if discountDetails['amountPaid'] >= discountDetails['weightAmount']:
        
        discountedPrice = discountDetails['amountPaid']-discount['discount']
        return {'discountedPrice':discountedPrice}
    
def setTieredDiscount(discountDetails: dict) -> dict:
        '''
        This function applies a tiered discount based on the total sale amount.
        
        @param discountDetails: A dictionary containing:
            - 'totalAmount': The total sale amount.
            - 'tiers': A list of tuples, each containing (min_amount, discount_rate)
        '''
        total_amount = discountDetails['totalAmount']
        tiers = discountDetails['tiers']
        
        # Initialize variables to track applicable discount
        applicable_discount = 0
        highest_discount_rate = None
        closest_discount_rate = None
        smallest_difference = float('inf')

        for min_amount, discount_rate in tiers:
            # Convert discount rate to float for calculation
            discount_value = calculateDiscount({'discountRate': discount_rate})['discount']
            
            if total_amount >= min_amount:
                # If the total amount exceeds this tier
                if highest_discount_rate is None or min_amount > highest_discount_rate[0]:
                    highest_discount_rate = (min_amount, discount_rate)

                # Check for the closest tier
                difference = total_amount - min_amount
                if difference < smallest_difference:
                    smallest_difference = difference
                    closest_discount_rate = discount_rate

        # Determine which discount to apply
        if highest_discount_rate:
            # Apply the highest discount if total_amount is greater than all
            print('>>>>>>>>>>>>>>>>>>highestDiscount rate',highest_discount_rate[1])
            applicable_discount = calculateDiscount({'discountRate': highest_discount_rate[1]})['discount'] * total_amount
        elif closest_discount_rate:
            # Otherwise, apply the closest discount
            print('>>>>>>>>>>>>>>>closestAmount',closest_discount_rate)
            applicable_discount = calculateDiscount({'discountRate': closest_discount_rate})['discount'] * total_amount

        # Calculate the final discounted price
        discounted_price = total_amount - applicable_discount

        return {
            'discountedPrice': discounted_price,
            'applicableDiscount': applicable_discount,
            'status': True if applicable_discount > 0 else False
        }

# --- the modules below are responsible for handling tickets 
def insertTicketIntoDb(ticketDetails:dict)->dict:
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        insertionResponse = db.insert('tickets',[ticketDetails['ticketId'],ticketDetails['ticket'],False])
        return insertionResponse 
    
def fetchTicketById(ticketDetails:dict)->dict:
    '''
        this function is responsible for fetching tickets by Id
        @param ticketDetails:'ticketId' is the expected key
    '''
    
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        response = db.fetch('tickets',['*'],condition="ticketId = ?",conditionData=[ticketDetails['ticketId']],limit=1,
                            returnDicts=True,returnNamespaces=False,parseJson=False,returnGenerator=False)
        if not len(response):
            return {'status':False, 'log':'This ticket doesn`t exist'}
        if response[0]['verified']:
            return {'status':False, 'log':'Ticket already Verified'}
        return {'status':True,'log':'','data':response}

def setVerificationStatus(ticketDetails:dict)->dict:
    '''
        this function is responsible for setting ticket
        verification status to true
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTables = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath,dbTables, readonly=False) as db:
        updateResponse = db.update('tickets',
                                   ['verified'],[True],'ticketId=?',[ticketDetails['ticketId']])
        return updateResponse
# def setTiredDiscount()          

# ----- the code below is responsible for handling cashdrawer reconciliation-------
def addOpeningBalanceToCashdrawer(openingDetails:dict)->dict:
    '''
        the expected keys for this function are 'entryId','timestamp','cashDrawerId','openingBalance'
        ,'closingBalance','openingBalance','others'
    '''
    entryId = 'entryId'+kutils.codes.new()
    timestamp = kutils.dates.currentTimestamp()
    date = kutils.dates.today()
    cashDrawerId = 'cashDrawerId'+kutils.codes.new()
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    table = kutils.config.getValue('bmsDb/tables')
    closingBalance = 0
    
    with kutils.db.Api(dbPath,table,readonly=False) as db:
        insertionResponse = db.insert('cashDrawer',
                                      [entryId,timestamp,date,cashDrawerId,openingDetails['openingBalance'],
                                       openingBalance['userName'],closingBalance,'notClosed','00-00-00',{}])
        return insertionResponse
    
def fetchCashDrawerByDate()->dict:
    '''
        this function is responsible for fetching  cashDrawer by details
        @param:none
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    table = kutils.config.getValue('bmsDb/tables')
    today = kutils.dates.today()
    
    with kutils.db.Api(dbPath,table,readonly=False) as db:
        fetchResponse = db.fetch('cashDrawer',['*'],'date=?',[today],limit=1,
                                 returnDicts=True,returnNamespaces=False,parseJson=False,returnGenerator=False)
    return fetchResponse
        
    
def  addClosingBalance(closingDetails:dict)->dict:
    '''
        this function  is responsible for updating the closing balance of the cashDrawer
        @param:'closingBalance','userName
    '''  
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    table = kutils.config.getValue('bmsDb/tables')
    timestamp = kutils.dates.currentTimestamp()
    date = kutils.dates.today()
    fetchResponse = fetchCashDrawerByDate()
    # dictToUpdate = fetchResponse[0]['others']
    # dictToUpdate = {'closingBalanceBy':closingDetails['userName'],'timeOfClosing':timestamp}
    with kutils.db.Api(dbPath,table,readonly=False) as db:
        updateResponse = db.update('cashDrawer',['closingBalance','closingBalanceBy','closingTime'],
                                   [closingDetails['closingBalance'],closingDetails['userName'],timestamp],
                                   'date=?',[date])
    return updateResponse
    

    
 
def init():
    defaults = {
        'rootPath':'/home/predator/Desktop/hbms',
        'dbName':'hbms',
        'tables':{
            "products":'''
                            productId           varchar (255) not null,
                            timestamp           varchar (255) not null,
                            userId              varchar (255) not null,
                            productName         varchar (255) not null,
                            productCategory     varchar (255) not null,
                            productCostPrice    integer (255) not null,
                            productSalePrice    integer (255) not null,
                            productQuantity     integer (255) not null,
                            units               varchar (255) not null,
                            productSerialNumber  varchar (255) not null,
                            productImage          varchar (255) not null,
                            others                 json,
                            discount               varchar(255) not null,
                            discountExpiry          varchar(255) not null
                          

            ''',
                'sales': '''
                            entryId             varchar(32) not null,
                            saleId              varchar(32) not null,
                            timestamp           varchar(24) not null,
                            dateSold            varchar(24) not null,
                            grandTotal          integer(32) not null,
                            numberOfItemsSold   integer(32) not null,
                            soldBy              varchar(32) not null,
                            soldTo              varchar(32) not null,
                            paymentType         varchar(32) not null,
                            paymentStatus      varchar(32) not null,
                            amountPaid          integer(32) not null,
                            others               json 
            ''',
                'productSales': '''
                                entryId     varchar(32) not null,
                                timestamp   varchar(32) not null,
                                dateSold    varchar(32) not null,
                                saleId      varchar(32) not null,
                                productId   varchar(32) not null,
                                unitPrice   integer(32) not null,
                                quantity    integer(32) not null,
                                units       varchar(32) not null,   
                                total       integer(32) not null,
                                others       json 
                                ''',
                'expenses':'''
                            entryId             varchar(32) not null,
                            timestamp           varchar(32) not null,
                            dateOfExpense       varchar(32) not null,
                            description         varchar(32) not null,
                            amountSpent         integer(32) not null,
                            others              json
                ''',
                'credits':'''
                            entryId         varchar(32) not null,
                            timestamp       varchar(32) not null,
                            creditId        varchar(32) not null,
                            saleId          varchar(32) not null,
                            soldBy          varchar(32) not null,
                            soldTo          varchar(32) not null,
                            amountInDebts   integer(32) not null,
                            paymentStatus  varchar(32) not null,
                            others           json
                ''',
                'customers':'''
                            entryId             varchar(32) not null,
                            timestamp           varchar(32) not null,
                            customerId          varchar(32) not null,
                            customerName        varchar(32) not null,
                            customerPhoneNumber integer(32) not null,
                            customerLocation    varchar(32) not null,
                            others              json
                            
                
                ''',
                'units':'''
                            entryId             varchar(32) not null,
                            timestamp           varchar(32) not null,
                            unitId              varchar(32) not null,
                            unit                varchar(32) UNIQUE not null,
                            others              json
                ''',
                'users':'''
                            entryId             varchar(32) not null,
                            timestamp           varchar(32) not null,
                            userId              varchar(32) not null,
                            userName            varchar(32) not null,
                            password            varchar(32) not null,
                            phoneNumber         integer(32) UNIQUE not null,
                            email               varchar(32) UNIQUE not null,
                            roleId              varchar(32) not null
                            
                
                ''',
                'revokeduser':'''
                                entryId     varchar(32) not null,
                                timestamp   varchar(32) not null,
                                userId      varchar(32) not null,
                                userName    varchar(32) not null,
                                password    varchar(32) not null,
                                phoneNumber integer(32) not null,
                                email       varchar(32) not null,
                                roleId      varchar(32) not null,
                                other       json
                
                ''',
                'roles':'''
                            entryId             varchar(32) not null,
                            timestamp           varchar(32) not null,
                            roleId              varchar(32) UNIQUE not null,
                            role                varchar(32) UNIQUE not null,
                            others              json
                
                ''',
                'categories':'''
                                entryId         varchar(32) not null,
                                timestamp       varchar(32) not null,
                                categoryId      varchar(32) not null,
                                category        varchar(32) UNIQUE not null,
                                others          json
                                
                ''',
                'cashDrawer':'''
                                entryId             varchar(32) not null,
                                timestamp           varchar(32) not null,
                                date                varchar(32) UNIQUE not null,
                                cashDrawerId        varchar(32) not null,
                                openingBalance      integer(32) not null,
                                openingBalanceBy    varchar(32) not null,
                                closingBalance      integer(32) not null,
                                closingBalanceBy    varchar(32) not null,
                                closingTime         varchar(32) not null,
                                others              json
                ''' ,
                'tickets':'''
                                ticketId    varchar(32) not null,
                                ticket      varchar(32) not null,
                                verified    boolean not null
                '''

        }
    }
    defaults['dbPath'] = defaults['rootPath']+'/db/'+defaults['dbName']
    config_topic = 'bmsDb'
    for key in defaults:
        if 1 or not kutils.config.getValue(config_topic+'/'+key):
            kutils.config.setValue(config_topic+'/'+key,defaults[key])
            
init()



if __name__ == "__main__":
   
    
    # g = kutils.permissions.Ok()
    
    product= {
        'productId':'pppp',
                            'timestamp':kutils.dates.currentTimestamp(),
                            'userId':kutils.codes.new(),
                            'productName':'shocks',
                            'productCategory':'brembo',
                            'productCostPrice':250000,
                            'productSalePrice':450000,
                            'productQuantity':10,
                            'units':'Pairs',
                            'productSerialNumber':'154258963',
                            'productImage':'tmp/static/angleyes.jpg',
                            'others':{}
    }
    singleProductSales = [
        {
            'entryId':kutils.codes.new(),
            'timestamp':kutils.dates.currentTimestamp(),
            'saleId':kutils.codes.new(),
            'productId':'dddd',
            'unitPrice':5000,
            'units':'pairs',
            'productQuantity':2,
            'total':2*5000,
            'others':{}
            
        },
         {
            'entryId':kutils.codes.new(),
            'timestamp':kutils.dates.currentTimestamp(),
            'saleId':kutils.codes.new(),
            'productId':'pppp',
            'unitPrice':5000,
            'units':'pairs',
            'productQuantity':2,
            'total':2*5000,
            'others':{}
            
        }
    ]
    productDetails = {       
                            'productId':'dddd',
                            'productName':'shocks',
                            'productCategory':'premium',
                            'productCostPrice':200000,
                            'productSalePrice':300000,
                            'productQuantity':20,
                            'units':'Pairs',
        
    }
    user = {
        'entryId':kutils.codes.new(),
        'timestamp':kutils.dates.currentTimestamp(),
        'userId':kutils.codes.new(),
        'userName':'Parrot',
        'password':'hello123',
        # 'roles':'MANAGER',
        'email':'adamzhakeam@gmail.com',
        'phoneNumber':'',
        'roleId':'Da9zqHxXnYwm'
    }
    
    aghi = {
        'phoneNumber':'0772462452',
        'other':{'revokedBy':'Parrot'}
    }
    expense = {
        'entryId':kutils.codes.new(),
        'timestamp':kutils.dates.currentTimestamp(),
        'dateOfExpense':kutils.dates.today(),
        'description':"Yaka",
        'amountSpent':80000,
        'others':{'user':'Karen'}
    }
    expense2 = {
        'dateOfExpense':'2024-09-02'
    }
    
    discountingDetails = {
        'productIds':['fYppObCw7JYX','iXW5FccFRdoj','GhXBcpwjVSqI'],
        'discountRate':'5000'
    }
    newRow = {
        'userId':'varchar(32) not null default xxx-xxx-xxx '
    }
    ticket = {
        'ticketId':"ticketId5bqOmjF6RxJk"
    }
    
    openingBalance = {
        'openingBalance':50000,
        'userName':'adamzkata'
    }
    
    closingDetails = {
        'closingBalance':70000,
        'userName':'sufraKagimu'
    }
    def insertNewColumn(newColn):
        dbPath = kutils.config.getValue('bmsDb/dbPath')
        dbTable = kutils.config.getValue('bmsDb/tables')
        
        with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
           response = db.alter('cashDrawer','userName','varchar(32) default xxxxxxxxx')
           return response 
    
    
    import pprint
    # print(fetchTicketById(ticket))
    # print(setVerificationStatus(ticket))
    # print(insertNewColumn(newRow))
    # print(fetchAllCustomers())
    # print(resetProductDiscountDetails()['updatedProducts'])
    # pprint.pprint(fetchAllProductsWithDiscount())
    # print(fetchSpecificProductById({'productId':'fYppObCw7JYX'}))
    # print(setProductFlatDiscountPrice(discountingDetails))
    pprint.pprint(fetchAllCustomers())  
    # print(createRoles({'role':'MANAGER','others':{}})) 
    # print(addOpeningBalanceToCashdrawer(openingBalance)) 
    # print(fetchCashDrawerByDate())
    # print(addClosingBalance(closingDetails))
    # print(createTables())
    # print(addExpenseToDb(expense))
    # print(fetchExpensesFromDb())
    # print(fetchSpecificExpenseByDate(expense2))
    # print(fetchAllProductSales())
    # print(fetchSpecificSalesFromTo({'dateFrom':'2024-08-16','dateTo':'2024-09-02'}))
    # print(fetchAllSales())
    # print(fetchSpecificProductSale({'saleDate':'2024-07-16'}))
    # print(fetchSpecificProductSalesFromTo({'dateFrom':'2024-08-16','dateTo':'2024-08-02'}))
    # print('>>>>>>>>>>>>',removeuserFromDb(aghi))
    # pprint.pprint(fetchAllusers())
    # print(fetchuserByPhoneNumber({'phoneNumber':'0772442222'})['log'][0]['userName'])
    # print(revokeuser(aghi))
    # print(fetchSpecificSale({'saleDate':'2024-07-09'}))
    # date = kutils.dates.today()
    # print(date)
    # print(createuser(user))
    # print(resetuserPassword({'phoneNumber':'0772442222'}))
    # print(login(user))
    # print(addSingleProductSale(singleProductSales))
    # print(insertProductIntoDb(product))
    # pprint.pprint(fetchSpecificProductById({'productId':'fYppObCw7JYX'}))
    # print(updateProductQuantity(si))
    # print(editParticularProduct(productDetails))
    # knockedUp print(fetchSpecificProduct({'productName':'angeleyes','productSerialNumber':'154258963'}))
    # print(addCategoryToDb({'category':'BREMBO','others':{}}))
    # print(fetchAllCustomers())
    
    
    
