from flask import Flask,request,jsonify
from flask_cors import CORS
import kisa_utils as kutils

app = Flask(__name__)
CORS(app)
# ---- these are routes to handle products activities in thw database ----
@app.route('/registerProduct',methods=['POST'])
def handleRegisterProduct():
    from . db import insertProductIntoDb
    '''
        this endpoint is responsible for inserting/registering
         product into the database 
    '''
    payload = request.get_json()
    payload['entryId'] = kutils.codes.new()
    payload['productId'] = kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payloadStructure = {
        'entryId':kutils.config.getValue('bmsDb/entryId'),
        'productId':kutils.config.getValue('bmsDb/productId'),
        'timestamp':kutils.config.getValue('bmsDb/timestamp'),
        'userId':kutils.config.getValue('bmsDb/userId'),
        'productName':kutils.config.getValue('bmsDb/productName'),
        'productCostPrice':kutils.config.getValue('bmsDb/productCostPrice'),
        'productSalePrice':kutils.config.getValue('bmsDb/productSalePrice'),
        'productSerialNumber':kutils.config.getValue('bmsDb/productSerialNumber'),
        'productCategory':kutils.config.getValue('bmsDb/productCategory'),
        'productQuantity':kutils.config.getValue('bmsDb/quantity'),
        'units':kutils.config.getValue('bmsDb/units'),
        'productImage':kutils.config.getValue('bmsDb/productImage')
        
    }
    
    productPayLoadvalidationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if productPayLoadvalidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return {
                    'status':False,
                    'log': f'the value for {key} is missing please provide it '
                }
    productinsertionresponse = insertProductIntoDb(payload)
    return jsonify(productinsertionresponse)

@app.route('/fetchAllProducts', methods=['POST'])
def handleFetchAllProducts():
    from . db import fetchAllProducts
    '''
        This endpoint is responsible for fetching all products from the database.
    '''
    response = fetchAllProducts()
    
    return jsonify(response)

@app.route('/fetchSpecificProduct', methods=['POST'])

def handleFetchSpecificProduct():
    from .db import fetchSpecificProduct
    '''
        This endpoint is responsible for fetching a specific product from the database.
    '''
    payload = request.get_json()
    productDetails = {
        'productName': payload.get('productName'),
        'productSerialNumber': payload.get('productSerialNumber')
    }
    
    if not productDetails['productName'] or not productDetails['productSerialNumber']:
        return jsonify({'status': False, 'log': 'Product name and serial number are required'}), 400

    response = fetchSpecificProduct(productDetails)
    
    return jsonify(response)

@app.route('/editProduct',methods=['POST'])
def handleEditProduct():
    '''
        this is endpoint function is responsible for editting a product
    '''
    from . db import editParticularProduct
    payload = request.get_json()
    
    payloadStructure = {
        'productId': kutils.config.getValue('bmsDb/productId'),
        'productName':kutils.config.getValue('bmsDb/productName'),
        'productCostPrice':kutils.config.getValue('bmsDb/productCostPrice'),
        'productSalePrice':kutils.config.getValue('bmsDb/productSalePrice'),
        'productCategory':kutils.config.getValue('bmsDb/productCategory'),
        'productQuantity':kutils.config.getValue('bmsDb/quantity'),
        'units':kutils.config.getValue('bmsDb/units'),
        
    }
    
    editProductValidationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if editProductValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return {
                    'status':False,
                    'log':f'the value for {key } is missing please provide it '
                }
        editResponse = editParticularProduct(payload)
        
        if not editResponse['status']:
            return jsonify(editResponse)
    return jsonify(editResponse)

# --- the routes below are responsible for handling database operations of sales
@app.route('/addSale', methods=['POST'])
def handleAddSale():
    '''
        This endpoint is responsible for adding an entire sale to the database.
    '''
    from .db import addSaleToDB
    payload = request.get_json()

    payload['entryId'] = kutils.codes.new()
    payload['saleId'] = kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()

    payloadStructure = {
        'entryId': kutils.config.getValue('bmsDb/entryId'),
        'saleId': kutils.config.getValue('bmsDb/saleId'),
        'timestamp': kutils.config.getValue('bmsDb/timestamp'),
        'grandTotal': kutils.config.getValue('bmsDb/grandTotal'),
        'numberOfItemsSold': kutils.config.getValue('bmsDb/numberOfItemsSold'),
        'soldBy': kutils.config.getValue('bmsDb/soldBy'),
        'soldTo': kutils.config.getValue('bmsDb/soldTo'),
        'paymentType': kutils.config.getValue('bmsDb/paymentType'),
        'paymentStatus': kutils.config.getValue('bmsDb/paymentStatus'),
        'amountPaid': kutils.config.getValue('bmsDb/amountPaid'),
        'others': kutils.config.getValue('bmsDb/others')
    }

    saleValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)

    if saleValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
        
        addSaleResponse = addSaleToDB(payload)
        
        if not addSaleResponse['status']:
            return jsonify(addSaleResponse)
    
    return jsonify(addSaleResponse)

@app.route('/addSingleProductSale', methods=['POST'])
def handleAddSingleProductSale():
    '''
        This endpoint is responsible for adding individual product sales to the database.
    '''
    from .db import addSingleProductSale
    payload = request.get_json()

    # Assuming payload is a list of single product sales
    for productSale in payload:
        productSale['entryId'] = kutils.codes.new()
        productSale['timestamp'] = kutils.dates.currentTimestamp()

    payloadStructure = {
        'entryId': kutils.config.getValue('bmsDb/entryId'),
        'timestamp': kutils.config.getValue('bmsDb/timestamp'),
        'saleId': kutils.config.getValue('bmsDb/saleId'),
        'productId': kutils.config.getValue('bmsDb/productId'),
        'unitPrice': kutils.config.getValue('bmsDb/unitPrice'),
        'units': kutils.config.getValue('bmsDb/units'),
        'productQuantity': kutils.config.getValue('bmsDb/productQuantity'),
        'total': kutils.config.getValue('bmsDb/total'),
        'others': kutils.config.getValue('bmsDb/others')
    }

    singleProductSaleValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)

    if singleProductSaleValidationResponse['status']:
        for productSale in payload:
            for key in productSale:
                if not productSale[key]:
                    return jsonify({
                        'status': False,
                        'log': f'The value for {key} is missing in one of the products. Please provide it.'
                    })
        
        addProductSalesResponse = addSingleProductSale(payload)
        
        if not addProductSalesResponse['status']:
            return jsonify(addProductSalesResponse)
    
    return jsonify(addProductSalesResponse)


 



def init():
    
        defaults = {
            'entryId':str,
            'productId':str,
            'timestamp':str,
            'userId':str,
            'productName':str,
            'productCostPrice':int,
            'productSalePrice':int,
            'productSerialNumber':str,
            'productCategory':str,
            'productQuantity':int,
            'units':str,
            'productImage':str,
            'unitPrice':int,
            'soldBy':str,
            'soldTo':str,
            'total':int,
            'grandTotal':int,
            'amountPaid':int,
            'payementType':str,
            'payementStatus':str,
            'numberOfItemsSold':str,
            
        }
        config_topic = 'bmsDb'
        
        for key in defaults:
            if 1 or not kutils.config.getValue(config_topic+'/'+key):
                kutils.config.setValue(config_topic+'/'+key,defaults[key])
                
init()
    