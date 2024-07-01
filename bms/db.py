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
        productInsertionResponse = db.insert(
            'products',
            [product['productId'],product['timestamp'],product['userId'],product['productName'],product['productCategory'],product['productCostPrice'],
             product['productSalePrice'],product['productQuantity'],product['units'],product['productSerialNumber'],product['productImage'],product['others']]
            
        )
        return productInsertionResponse
    
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
        if operation i snot successful it returns False as status and the log contains the error 
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
            ['productName','productCategory','productCostPrice','productSalePrice','productSalePrice','productQuantity',
             'units','productSerialNumber','productImage'],
            'productName = ? and productSerialNumber = ?',
            [productDetails['productName'],productDetails['productSerialNumber']],
            limit = 10,
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
            [sales['entryId'], sales['saleId'], sales['timestamp'], sales['grandTotal'], sales['numberOfItemsSold'], 
             sales['soldBy'],sales['soldTo'],sales['paymentType'], sales['paymentStatus'], sales['amountPaid'],sales['others']])
        return insertSaleStatus
    
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
                    [productSale['entryId'], productSale['timestamp'], productSale['saleId'], productSale['productId'], 
                     productSale['unitPrice'], productSale['units'], productSale['productQuantity'], productSale['total'], productSale['others']]
                )
                # updateProductQuantity(productSale)
                
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

# ---- the modules below are responsible for handlng users-----

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
            [roleDetails['entryId'],roleDetails['timestamp'],roleDetails['roleId'],roleDetails['others']]
        )
        return roleInsertionResponse
    
def fetchRole(roleId:str)->list:
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
            [roleId],
            limit = 1,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator= False
        )
        return roleFetchResults
    




             
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
                            grandTotal          integer(32) not null,
                            numberOfItemsSold   integer(32) not null,
                            soldBy              varchar(32) not null,
                            soldTo              varchar(32) not null,
                            paymentType         varchar(32) not null,
                            paymentStatus      varchar(32) not null,
                            amountPaid          varchar(32) not null,
                            others               json 
            ''',
                'productSales': '''
                                entryId     varchar(32) not null,
                                timestamp   varchar(32) not null,
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
                            amountInDebts   varchar(32) not null,
                            payementStatus  varchar(32) not null,
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
    # print(createUser(user))
    # print(login(user))
    print(addSingleProductSale(singleProductSales))
    print(insertProductIntoDb(product))
    # print(fetchAllProducts())
    # print(updateProductQuantity(si))
    # print(editParticularProduct(productDetails))
    # print(fetchSpecificProduct({'productName':'angeleyes','productSerialNumber':'154258963'}))
    