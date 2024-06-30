from flask import Flask,request,jsonify,session, redirect, url_for
from functools import wraps
# from flask_Ses
from flask_cors import CORS
import kisa_utils as kutils
from flask_session import Session
import os

app = Flask(__name__)
CORS(app)
app.config['SECRETE_KEY'] = kutils.config.getValue('bmsDb/SECRETE_KEY')
app.config['SESSION_TYPE'] = kutils.config.getValue('bmsDb/SESSION_TYPE')
app.config['SESSION_PERMANENT'] = kutils.config.getValue('bmsDb/SESSION_PERMANENT')
app.config['SESSION_USER_SIGNER'] = kutils.config.getValue('bmsDb/SESSION_USER_SIGNER')
Session(app)

# this function is responsible for protecting routes 
def loginRequired(role):
    def wrapper(func):
        @wraps(func)
        def decoratedView(*args,**kwargs):
            from db import fetchRole
            if 'roleId' in session:
                roleList = fetchRole(session['roleId'])
                userRole = roleList[0]['role']
                if userRole == role:
                    return func(*args,**kwargs)
                return jsonify({'status':False, 'log':f'{role} is not authorized '})
            return{'status':False,'log':'roleId required to grant access'}
        return decoratedView
    return wrapper
            
# ---- these are routes to handle products activities in thw database ----
@app.route('/registerProduct',methods=['POST'])
def handleRegisterProduct():
    from db import insertProductIntoDb
    '''
        this endpoint is responsible for inserting/registering
         product into the database 
    '''
    payload = request.get_json()
    payload['entryId'] = kutils.codes.new()
    payload['productId'] = kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payload['userId'] = "sirkata"
    payload['others'] = {}
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
        'productImage':kutils.config.getValue('bmsDb/productImage'),
        'others':kutils.config.getValue('bmsDb/others')
        
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
    from db import fetchAllProducts
    '''
        This endpoint is responsible for fetching all products from the database.
    '''
    response = fetchAllProducts()
    
    return jsonify(response)

@app.route('/fetchSpecificProduct', methods=['POST'])

def handleFetchSpecificProduct():
    from db import fetchSpecificProduct
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
@loginRequired('admin')
def handleEditProduct():
    '''
        this is endpoint function is responsible for editting a product
    '''
    from db import editParticularProduct
    payload = request.get_json()
    
    payloadStructure = {
        'productId': kutils.config.getValue('bmsDb/productId'),
        'productName':kutils.config.getValue('bmsDb/productName'),
        'productCostPrice':kutils.config.getValue('bmsDb/productCostPrice'),
        'productSalePrice':kutils.config.getValue('bmsDb/productSalePrice'),
        'productCategory':kutils.config.getValue('bmsDb/productCategory'),
        'productQuantity':kutils.config.getValue('bmsDb/productQuantity'),
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
        print(payload[key])
        print('____',editParticularProduct(payload))
        editResponse = editParticularProduct(payload)
        print(editResponse)
        
        if not editResponse['status']:
            return jsonify(editResponse)
    return jsonify(editProductValidationResponse)

# --- the routes below are responsible for handling database operations of sales
@app.route('/addSale', methods=['POST'])
def handleAddSale():
    '''
        This endpoint is responsible for adding an entire sale to the database.
    '''
    from db import addSaleToDB
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
    from db import addSingleProductSale
    payload = request.get_json()
    print('payload',payload)
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

# ------the module below is responsible fo handling user and roles  related endpoints 

@app.route('/addUser',methods=['POST'])
def handleAdduser():
    '''
    this function is responsible for handling 
    the adduser endpoint 
    '''
    from db import createUser
    payload = request.get_json()
    payload['entryId'] = kutils.codes.new()
    payload['userId'] = kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payloadStructure = {
        'entryId':kutils.config.getValue('bmsDb/entryId'),
        'timestamp':kutils.config.getValue('bmsDb/timestamp'),
        'userId':kutils.config.getValue('bmsDb/userId'),
        'userName':kutils.config.getValue('bmsDb/userName'),
        'password':kutils.config.getValue('bmsDb/password'),
        'email':kutils.config.getValue('bmsDb/email'),
        'phoneNumber':kutils.config.getValue('bmsDb/phoneNumber'),
        # 'roles':kutils.config.getValue('bmsDb/roles'),
        'roleId':kutils.config.getValue('bmsDb/roleId')
    }
    validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if validationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
        
        createUserResponse  = createUser(payload)
        
        if not createUserResponse['status']:
            return jsonify(createUserResponse)
    
    return jsonify(validationResponse)
@app.route('/login',methods=['POST'])
def handlelogin():
    from db import login
    payload = request.get_json()
    payloadStructure = {
        'phoneNumber':kutils.config.getValue('bmsDb/phoneNumber'),
        'password':kutils.config.getValue('bmsDb/password')
    }
    loginValidationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    if loginValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
        
        loginResponse  = login(payload)
        
        if loginResponse['status']:
            user = loginResponse['log'][0]
            session['userId'] = user['userId']
            session['userName'] = user['userName']
            session['roleId'] = user['roleId']
            
    
        return  jsonify(loginResponse)
    return jsonify(loginValidationResponse)

@app.route('/profile')
def profile():
    if 'userId' in session:
        userId = session['userId']
        userName = session['userName']
        roleId = session['roleId']
        
        return jsonify({'userId':userId,'userName':userName,'role':roleId})
    return jsonify({'status':False,'log':'User is not logged in'})

@app.route('/logoutUser')
def handleLogoutUser():
    session.clear()
    return jsonify({'status':True, 'log':'Logged Out Successfully'}) 



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
            'userId':str,
            'userName':str,
            'phoneNumber':str,
            'roles':str,
            'email':str,
            'roleId':str,
            'password':str,
            'role':str,
            'others':str,
            'SECRETE_KEY':os.urandom(24),
            'SESSION_TYPE':'filesystem',
            'SESSION_PERMANENT':False,
            'SESSION_USER_SIGNER':True
            
        }
        config_topic = 'bmsDb'
        
        for key in defaults:
            if 1 or not kutils.config.getValue(config_topic+'/'+key):
                kutils.config.setValue(config_topic+'/'+key,defaults[key])
                
init()

if __name__ == "__main__":
     app.run(debug=True,host = '0.0.0.0',port = 5000)