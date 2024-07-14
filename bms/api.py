from flask import Flask,request,jsonify,session, redirect, url_for
from functools import wraps
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
            
# ---- these are routes to handle products activities in the database ----
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
        'productName': payload.get('productName')
    }
    
    if not productDetails['productName'] :
        return jsonify({'status': False, 'log': 'Product name and serial number are required'}), 400

    response = fetchSpecificProduct(productDetails)
    
    return jsonify(response)

@app.route('/fetchSpecificProductById', methods=['POST'])

def handleFetchSpecificProductById():
    from db import fetchSpecificProductById
    '''
        This endpoint is responsible for fetching a specific product from the database.
    '''
    payload = request.get_json()
    productDetails = {
        # 'productName': payload.get('productName'),
        'productId': payload.get('productId')
    }
    print(payload)
    if not productDetails['productId']:
        return jsonify({'status': False, 'log': ' productId is required'}), 400

    response = fetchSpecificProductById(productDetails)
    print(response)
    
    return jsonify(response)

@app.route('/fetchSpecificProductByCategory', methods=['POST'])

def handleFetchSpecificProductByCategory():
    from db import fetchSpecificProductByCategory
    '''
        This endpoint is responsible for fetching a specific product from the database.
    '''
    payload = request.get_json()
    productDetails = {
        # 'productName': payload.get('productName'),
        'productCategory': payload.get('productCategory')
    }
    
    if not productDetails['productCategory']:
        return jsonify({'status': False, 'log': ' productId is required'}), 400

    response = fetchSpecificProductByCategory(productDetails)
    print(response)
    
    return jsonify(response)


@app.route('/fetchSpecificProductByPertNumber', methods=['POST'])

def handleFetchSpecificProductByPertNumber():
    from db import fetchSpecificProductByPn
    '''
        This endpoint is responsible for fetching a specific product from the database.
    '''
    payload = request.get_json()
    productDetails = {
        # 'productName': payload.get('productName'),
        'productSerialNumber': payload.get('productSerialNumber')
    }
    
    if not productDetails['productSerialNumber']:
        return jsonify({'status': False, 'log': 'Product  product pert number is required'}), 400

    response = fetchSpecificProductByPn(productDetails)
    print(response)
    
    return jsonify(response)



@app.route('/editProduct',methods=['POST'])
# @loginRequired('admin')
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
'''
    this module is responsible for handling routes for the sales module 
    these include these include fetching,editing,deleting and adding
'''
@app.route('/addSale', methods=['POST'])
def handleAddSale():
    '''
        This endpoint is responsible for adding an entire sale to the database.
    '''
    from db import addSaleToDB,addCreditDetailsToDb
    payload = request.get_json()

    payload['entryId'] = kutils.codes.new()
    payload['saleId'] = 'saleId'+kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payload['dateSold'] = kutils.dates.today()

    payloadStructure = {
        'entryId': kutils.config.getValue('bmsDb/entryId'),
        'saleId': kutils.config.getValue('bmsDb/saleId'),
        'timestamp': kutils.config.getValue('bmsDb/timestamp'),
        'dateSold': kutils.config.getValue('bmsDb/dateSold'),
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
                
        print('addsalepayload',payload)
        addSaleResponse = addSaleToDB(payload)
        
        if not addSaleResponse['status']:
            return jsonify(addSaleResponse)
        # print('!!!!!!!!!!!!!!!!===>patch',payload['saleId'])
        addCreditDetailsResponse = addCreditDetailsToDb(payload)
        print('cerdit',addCreditDetailsResponse)
        return {'status':True,'log':'sale added succesfully','saleId':payload['saleId']}
    
    return jsonify(saleValidationResponse)

@app.route('/fetchAllSales', methods=['POST'])
def handleFetchAllSales():
    from db import fetchAllSales
    '''
        This endpoint is responsible for fetching all sales from the database.
    '''
    response = fetchAllSales()
    
    return jsonify(response)

@app.route('/fetchSpecificSales', methods=['POST'])

def handleFetchSaleOnSpecificDate():
    from db import fetchSpecificSale
    '''
        This endpoint is responsible for fetching a specific sales on a specific date from the database.
    '''
    payload = request.get_json()
    saleDetails = {
        'saleDate': payload.get('saleDate'),
        
    }
    
    if not saleDetails['saleDate']:
        return jsonify({'status': False, 'log': 'Sale Date are required'}), 400

    response = fetchSpecificSale(saleDetails)
    
    return jsonify(response)
@app.route('/fetchSpecificSalesFromTo', methods=['POST'])

def handleFetchSaleOnSpecificDateFromTo():
    from db import fetchSpecificSalesFromTo
    '''
        This endpoint is responsible for fetching a specific sales on a specific date from the database.
    '''
    payload = request.get_json()
    saleDetails = {
        'dateFrom': payload.get('dateFrom'),
        'dateTo':payload.get('dateTo')
        
    }
    
    if not saleDetails['saleDate']:
        return jsonify({'status': False, 'log': 'Sale Date are required'}), 400

    response = fetchSpecificSalesFromTo(saleDetails)
    
    return jsonify(response)

@app.route('/addSingleProductSale', methods=['POST'])
def handleAddSingleProductSale():
    '''
    This endpoint is responsible for adding individual product sales to the database.
    '''
    from db import addSingleProductSale
    
    
    payload = request.get_json()
    # workingSaleId = handleAddSale()
    # print(workingSaleId)
    # payload['saleId'] = workingSaleId['saleId']
    print('Received payload:', payload)  # Debug: Print received payload

    if not payload:
        return jsonify({'status': False, 'log': 'No data provided'}), 400
    
    # Assuming payload is a list of single product sales
    for productSale in payload:
        productSale['entryId'] = kutils.codes.new()
        productSale['timestamp'] = kutils.dates.currentTimestamp()
        productSale['dateSold'] = kutils.dates.today()
    
    print('Payload after adding entryId and timestamp:', payload)  # Debug: Print modified payload
    
    payloadStructure = [{
        'entryId': kutils.config.getValue('bmsDb/entryId'),
        'timestamp': kutils.config.getValue('bmsDb/timestamp'),
        'saleId': kutils.config.getValue('bmsDb/saleId'),
        'productId': kutils.config.getValue('bmsDb/productId'),
        'unitPrice': kutils.config.getValue('bmsDb/unitPrice'),
        'units': kutils.config.getValue('bmsDb/units'),
        'productQuantity': kutils.config.getValue('bmsDb/productQuantity'),
        'total': kutils.config.getValue('bmsDb/total'),
        'others': kutils.config.getValue('bmsDb/others')
    }]
    
    singleProductSaleValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)
    print('Validation response:', singleProductSaleValidationResponse)  # Debug: Print validation response
    
    if not singleProductSaleValidationResponse['status']:
        return jsonify(singleProductSaleValidationResponse)
    
    for productSale in payload:
        for key in productSale:
            if not productSale[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing in one of the products. Please provide it.'
                }), 400
    
    addProductSalesResponse = addSingleProductSale(payload)
    print('Database insertion response:', addProductSalesResponse)  # Debug: Print DB response
    
    if not addProductSalesResponse['status']:
        return jsonify(addProductSalesResponse)
    
    return jsonify({'status': True, 'log': 'Products added successfully!'})

@app.route('/fetchAllProductSales', methods=['POST'])
def handleFetchAllProductSales():
    from db import fetchAllProductSales
    '''
        This endpoint is responsible for fetching all product sales from the database.
    '''
    response = fetchAllProductSales()
    
    return jsonify(response)

@app.route('/fetchSpecificProductSales', methods=['POST'])

def handleFetchProductSaleOnSpecificDate():
    from db import fetchSpecificProductSale
    '''
        This endpoint is responsible for fetching a specific sales on a specific date from the database.
    '''
    payload = request.get_json()
    saleDetails = {
        'saleDate': payload.get('saleDate'),
        
    }
    
    if not saleDetails['saleDate']:
        return jsonify({'status': False, 'log': 'Sale Date are required'}), 400

    response = fetchSpecificProductSale(saleDetails)
    
    return jsonify(response)
@app.route('/fetchSpecificProductSalesFromTo', methods=['POST'])

def handleFetchProductSaleOnSpecificDateFromTo():
    from db import fetchSpecificProductSalesFromTo
    '''
        This endpoint is responsible for fetching a specific sales on a specific date from the database.
    '''
    payload = request.get_json()
    saleDetails = {
        'dateFrom': payload.get('dateFrom'),
        'dateTo':payload.get('dateTo')
        
    }
    
    if not saleDetails['saleDate']:
        return jsonify({'status': False, 'log': 'Sale Date are required'}), 400

    response = fetchSpecificProductSalesFromTo(saleDetails)
    
    return jsonify(response)



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
        'roles':kutils.config.getValue('bmsDb/roles'),
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

@app.route('/fetchAllUsers',methods=['POST'])
def handleFetchAllUsers():
    from db import fetchAllUsers
    
    response = fetchAllUsers()
    return jsonify(response)

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

# ---the module below is responsible for handling all the credit endpoints
# -------module for credit endpoints-----------

@app.route('/fetchAllCredits',methods=['POST'])
def handleFetchAllCredits():
    from db import fetchAllCredits
    
    response = fetchAllCredits()
    return jsonify(response)

@app.route('/editCredit',methods = ['POST'])
def handleEditCredit():
    from db import editCredit
    payload = request.get_json()
    print('....payload recieved',payload)
    payloadStructure = {
        # 'timestamp':kutils.dates.currentTimestamp(),
        'amountPaid':kutils.config.getValue('bmsDb/amountPaid'),
        'saleId':kutils.config.getValue('bmsDb/saleId'),
        'creditId':kutils.config.getValue('bmsDb/creditId'),
        'paymentStatus':kutils.config.getValue('bmsDb/paymentStatus'),
        # 'amountInDebt':kutils.config.getValue('bmsDb/amountInDebt')
        # 'editedBy':kutils.config.getValue('bmsDb/editedBy')
    }
    payloadValidationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if payloadValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({
                    'status':False,
                    'log':f'the value for {key} is missing please provide it '
                })
        print('....',payload)
        creditEditingResponse = editCredit(payload)
        return jsonify(creditEditingResponse)
    return jsonify(payloadValidationResponse)

# ------below these endpoints handle roles --
@app.route('/createRole',methods=['POST'])
def handleCreateRole():
    '''
        this endpoint is responsible for creating a a role 
        
    '''
    from db import createRoles
    payload = request.get_json()
    payload['entryId'] = kutils.codes.new()
    payload['roleId'] = kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payloadStructure = {
        'entryId':kutils.config.getValue('bmsDb/entryId'),
        'timestamp':kutils.config.getValue('bmsDb/timestamp'),
        'roleId':kutils.config.getValue('bmsDb/roleId'),
        'role':kutils.config.getValue('bmsDb/role'),
        'others':kutils.config.getValue('bmsDb/others')
       
    }
    validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if validationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
        
        createRoleResponse  = createRoles(payload)
        
        if not createRoleResponse['status']:
            return jsonify(createRoleResponse)
    
    return jsonify(validationResponse)

@app.route('/fetchAllRoles',methods=['POST'])
def handleFetchAllRoles():
    from db import fetchAllRoles
    
    response = fetchAllRoles()
    return jsonify(response)

@app.route('/fetchRole',methods=['POST'])
def handleFetchRole():
    from db import fetchRole
    payload = request.get_json()
    payloadStructure = {
        'roleId':kutils.config.getValue('bmsDb/roleId'),
    }
    validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if validationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
        
        createRoleResponse  = fetchRole(payload)
        
        if not createRoleResponse['status']:
            # print(createRoleResponse)
            return jsonify(createRoleResponse)
    
    return jsonify(validationResponse)

# --this module is responsible handing all the category endpoints 
@app.route('/fetchAllCategories',methods = ['POST'])
def handleFetchAllCategories():
    from db import fetchAllCategories
    
    response = fetchAllCategories()
    return jsonify(response)    
  
@app.route('/createCategory',methods=['POST'])
def handleCreateCategory():
    from db import addCategoryToDb
    payload = request.get_json()
    payload['entryId'] = kutils.codes.new()
    payload['categoryId'] = kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payloadStructure = {
        'entryId':kutils.config.getValue('bmsDb/entryId'),
        'timestamp':kutils.config.getValue('bmsDb/timestamp'),
        'categoryId':kutils.config.getValue('bmsDb/categoryId'),
        'category':kutils.config.getValue('bmsDb/category'),
        'others':kutils.config.getValue('bmsDb/others')
       
    }
    validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if validationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
        
        createRoleResponse  = addCategoryToDb(payload)
        
        if not createRoleResponse['status']:
            return jsonify(createRoleResponse)
    
    return jsonify(validationResponse)

    



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
            'categoryId':str,
            'category':str,
            'productQuantity':int,
            'units':str,
            'productImage':str,
            'unitPrice':int,
            'soldBy':str,
            'soldTo':str,
            'total':int,
            'grandTotal':int,
            'amountPaid':int,
            'editedBy':str,
            'paymentType':str,
            'paymentStatus':str,
            'numberOfItemsSold':int,
            'dateSold':str,
            'userId':str,
            'userName':str,
            'phoneNumber':str,
            'roles':str,
            'email':str,
            'roleId':str,
            'password':str,
            'role':str,
            'creditId':str,
            'others':dict,
            'saleId':str,
            'amountInDebt':int,
            'SECRETE_KEY':kutils.codes.new(),
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