''''
        the modules below are responsible for handling the database processes of the 
        business management system 
'''
import kisa_utils as kutils

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
                    'productSerialNumber','productImage','others'
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbtable = kutils.config.getValue('bmsDb/tables')
    
    # productId,timestamp,userId,productName,productCategory,productCostPrice,productSalePrice,productQuantity,units,productSerialNumber,productImage,others = product.values()
    with kutils.db.Api(dbPath, dbtable, readonly=False ) as db:
        fetchProductByPertNumber = fetchSpecificProductByPn(product)
        fetchProductByCategory = fetchSpecificProductByCategory(product)
        if not fetchProductByPertNumber['status'] or not fetchProductByCategory['status']:
            
            productInsertionResponse = db.insert(
                'products',
                [product['productId'],product['timestamp'],product['userId'],product['productName'],product['productCategory'],product['productCostPrice'],
                product['productSalePrice'],product['productQuantity'],product['units'],product['productSerialNumber'],product['productImage'],product['others']]
                
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
             'units','productSerialNumber','productImage'],
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
            limit = 5,
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
    
def createTables():
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTables = kutils.config.getValue('bmsDb/tables')
    
    with kutils.db.Api(dbPath,dbTables, readonly=False) as db:
        creationResponse = db.createTables(dbTables)
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
    # entryId, saleId, timestamp, grandTotal, numberOfItemsSold, soldBy,soldTo,payementType,payementStatus,amountPaid, others = sales.values()

    with kutils.db.Api(dbPath, dbTable, readonly=False)as db:
        insertSaleStatus = db.insert(
            "sales", 
            [sales['entryId'], sales['saleId'], sales['timestamp'],sales['dateSold'], sales['grandTotal'], sales['numberOfItemsSold'], 
             sales['soldBy'],sales['soldTo'],sales['paymentType'], sales['paymentStatus'], sales['amountPaid'],sales['others']])
        return insertSaleStatus
    
def fetchSpecificSale(saleDetails:dict) -> list:
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

def fetchSpecificSaleById(saleDetails:dict) -> list:
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

    
def fetchSpecificSalesFromTo(saleDates:dict) -> list:
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
            ['grandTotal','numberOfItems','soldBy','soldTo','paymentType','paymentStatus','amountPaid'],
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
    

    
def fetchAllSales()->list:
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
                updateProductQuantity(productSale)
                # print('productSubResp',response) 
                
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

def createUser(userDetails:dict)->dict:
    '''
        this module is responsible for creation of a user 
        @param userDetails:'entryId','timestamp','userId','userName','password',
                            'phoneNumber','roleId','email' are the expected keys 
        returns a dictionary with status and log 
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    passwordHash = kutils.encryption.hash(userDetails['password'])
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
            [userDetails['entryId'],userDetails['timestamp'],userDetails['userId'],userDetails['userName'],
             passwordHash,userDetails['phoneNumber'],userDetails['email'],userDetails['roleId']]
        )
    return(userCreationResponse)

def fetchAllUsers()->list:
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
    

def login(userDetails:dict)->dict:
    '''
        this function is responsible for verifying credentials from the front end 
        @param userDetails:'phoneNumber','password' are the expected keys  
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    passwordHash = kutils.encryption.hash(userDetails['password'])
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        userFetchResponse = db.fetch(
            'users',
            ['userId','userName','phoneNumber','password','roleId'],'phoneNumber=? and password=?',
            [userDetails['phoneNumber'],passwordHash],
            limit = 1,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator=False
        )
        if len(userFetchResponse) > 0:
            return {'status':True, 'log':userFetchResponse}
        return{'status':False, 'log':'You have input a wrong password'}
    

def createRoles(roleDetails:dict)->dict:
    '''
        this module is responsible for creation of roles and adding them to the db
        @param roleDetails:'entryId','timestamp','roleId','role','others'
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        roleInsertionResponse = db.insert(
            'roles',
            [roleDetails['entryId'],roleDetails['timestamp'],roleDetails['roleId'],roleDetails['role'],roleDetails['others']]
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
        print(roleFetchResults)
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
    
    
def fetchCustomerById(customerId:str)->list:
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
            [customerId],limit = 1,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        return customerFetchResponse

# ----the module below handles product categories----
'''
    this module is responsible for adding and fetching 
    product categories to and from the database 
'''
def addCategoryToDb(categoryDetails:dict)->dict:
    '''
        this function is responsible for adding category to Db
        @param categoryDetails:'entryId','timestamp','categoryId','category',others are the expected keys
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbTable = kutils.config.getValue('bmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
        categoryFetchResponse = db.fetch(
            'categories',
            ['category'],
            'category = ?',
            [categoryDetails['category']],limit = 1,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        if len(categoryFetchResponse) > 0:
            return{'status':False, 'log':f'{categoryDetails["category"]} has already been registered'}
    

        categoryInsertionResponse = db.insert(
            'categories',
            [categoryDetails['entryId'],categoryDetails['timestamp'],categoryDetails['categoryId'],
             categoryDetails['category'],categoryDetails['others']]
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
                 'log':f"there is no category rigesterd under the name{categoryName}"
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
    if len(specificProductSaleFetchResponse) == 0:
        return{
            'status':False,
            'log':specificProductSaleFetchResponse
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

        

        

             
def init():
    defaults = {
        'rootPath':'/tmp/hbms',
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
                            others                 json
                          

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
                'users':'''
                            entryId             varchar(32) not null,
                            timestamp           varchar(32) not null,
                            userId              varchar(32) not null,
                            userName            varchar(32) not null,
                            password            varchar(32) not null,
                            phoneNumber         integer(32) not null,
                            email               varchar(32) not null,
                            roleId              varchar(32) not null
                            
                
                ''',
                'roles':'''
                            entryId             varchar(32) not null,
                            timestamp           varchar(32) not null,
                            roleId              varchar(32) not null,
                            role                varchar(32) not null,
                            others              json
                
                ''',
                'categories':'''
                                entryId         varchar(32) not null,
                                timestamp       varchar(32) not null,
                                categoryId     varchar(32) not null,
                                category        varchar(32) not null,
                                others          json
                                
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
        'userName':'johndoe',
        'password':'hello123',
        'roles':'user',
        'email':'johndoe@gmail.com',
        'phoneNumber':256782345678,
        'roleId':'user'
    }
   
    createTables()
    # print(fetchSpecificSale({'saleDate':'2024-07-09'}))
    # date = kutils.dates.today()
    # print(date)
    # print(createUser(user))
    # print(login(user))
    # print(addSingleProductSale(singleProductSales))
    # print(insertProductIntoDb(product))
    # print(fetchAllProducts())
    # print(updateProductQuantity(si))
    # print(editParticularProduct(productDetails))
    # print(fetchSpecificProduct({'productName':'angeleyes','productSerialNumber':'154258963'}))
    