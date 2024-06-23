import kisa_utils as kutils
# ----- below is code to handle products-----
def insertProductIntoDb(product:dict)->dict:
    '''
        this function is responsible for inserting product into the database 
        @param product: 'productId','timestamp','userId','productName',productCategory,
                    'productCostPrice','productSalePrice','productQuantity','units',
                    'productSerialNumber','productImage','others'
    '''
    dbPath = kutils.config.getValue('bmsDb/dbPath')
    dbtable = kutils.config.getValue('bmsDb/tables')
    
    productId,timestamp,userId,productName,productCategory,productCostPrice,productSalePrice,productQuantity,units,productSerialNumber,productImage,others = product.values()
    with kutils.db.Api(dbPath, dbtable, readonly=False ) as db:
        productInsertionResponse = db.insert(
            'products',
            [productId,timestamp,userId,productName,productCategory,productCostPrice,
             productSalePrice,productQuantity,units,productSerialNumber,productImage,others]
            
        )
        return productInsertionResponse
    
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
        'productId':kutils.codes.new(),
                            'timestamp':kutils.dates.currentTimestamp(),
                            'userId':kutils.codes.new(),
                            'productName':'shocks',
                            'productCategory':'brembo',
                            'productCostPrice':15000,
                            'productSalePrice':25000,
                            'productQuantity':10,
                            'units':'Pairs',
                            'productSerialNumber':'154258963',
                            'productImage':'tmp/static/bremboshocks.jpg',
                            'others':{}
    }
    
    createTables()
    # print(insertProductIntoDb(product))
    # print(fetchAllProducts())
    print(fetchSpecificProduct({'productName':'shocks','productSerialNumber':'154258963'}))