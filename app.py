from flask import Flask,request,jsonify,session, redirect, url_for,render_template,make_response,send_file
# from flask_sqlalchemy import SQL
from functools import wraps
from flask_cors import CORS
import kisa_utils as kutils
#import jwt
from datetime import datetime, timedelta
from auth_utils import generate_token, decode_token
from flask_mail import Mail, Message
from datetime import datetime
from openpyxl import Workbook
# import logging
# import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = kutils.config.getValue('bmsDb/SECRETE_KEY')
# Configure Flask-Mail with your SMTP server details
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587 #465
app.config['MAIL_userNAME'] = kutils.config.getValue('bmsDb/email')#  # Your email
app.config['MAIL_PASSWORD'] = kutils.config.getValue('bmsDb/mailPassword')   # Your email password or app-specific password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False 

mail = Mail(app)

@app.route("/sendMail", methods=['POST'])
def sendMail():
    '''
    This endpoint is responsible for sending emails
    '''
    payload = request.get_json()
    if not payload:
        return jsonify({'status': False, 'log': 'Payload is missing or invalid'})
    
    print(f"Payload received: {payload}")
    
    payloadStructure = {
        'subject': kutils.config.getValue('bmsDb/subject'),
        'recipients': kutils.config.getValue('bmsDb/recipients'),
        'message': kutils.config.getValue('bmsDb/message')
    }
    
    payloadValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)
    # print(f"Payload validation status: {payloadValidationResponse['status']}")
    
    if payloadValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({'status': False, 'log': f"The value for {key} is missing, please provide it"})
        
        # print(f"Recipients: {payload.get('recipients')}")
        
        
        for recipient in payload['recipients']:
            # print('>>>> Running recipient loop')
            if not isinstance(recipient, str):
                return jsonify({'status': False, 'log': f"The recipient {recipient} expects strings in the list"})
        
        msg = Message(
            payload['subject'],
            sender='your business Point Of Sale System',
            recipients=payload['recipients']
        )
        msg.body = payload['message']
        
        with app.app_context():
            mail.send(msg)
        
        return jsonify({'status': True, 'log': ''})
    
    return jsonify(payloadValidationResponse)

def sendDynamicMail(mailDetails:dict)->dict:
    '''
        this function is responsible for sending emails
        the expected keys are 'recipients','message','subject','imagePath'
    '''
    print('>>>>>>>',len(mailDetails['recipients']))
    if not len(mailDetails['recipients']):
        return jsonify({'status':False,'log':'no recipients to sendmail to '})
    msg = Message(
            mailDetails['subject'],
            sender='your business Point Of Sale System',
            recipients=mailDetails['recipients']
        )
    msg.body = mailDetails['message']
    if len(mailDetails['imagePath']):
        with app.open_resource(mailDetails['imagePath'][0]) as qr:
            msg.attach('ticket_adamzKata.png','image/png', qr.read())
        mail.send(msg)
        return {'status':True, 'log':'sent with an attachement'}
    with app.app_context():
            mail.send(msg)
        
    return jsonify({'status': True, 'log': ''})

@app.route('/')
def home():
    # create the database tables if they don't exist 
    from db import createTables
    createTables()
    
    # Renders the index.html file located in the templates folder
    
    return render_template('index.html')

# -----endpoints to verify ticket 
@app.route('/verifyQr', methods=['POST'])
def verifyQr():
    from tickets import verifyTicket
    # Get the entire JSON payload
    qrData = request.get_json()
    # Extract the 'qr_data' value from the dictionary
    qrString = qrData.get('qr_data')
    
    # Ensure qrString is not None and then split it
    if qrString:
        ticketId, receivedHash = qrString.split('|')
        response = verifyTicket({'ticketId': ticketId})
        return jsonify(response)
    else:
        return jsonify({'status': False, 'log': 'Invalid QR data'}), 400

    

# ----------------------------the endpoint below is responsible for resetting product discount ---
@app.route('/resetProductDiscount',methods=['POST'])
def resetProductDiscount():
    '''
        this endpoint is responsible for resetting product discount
        and then sending mail to the MANAGER for the updated discounts  
    '''
    from db import resetProductDiscountDetails
    resetResponse = resetProductDiscountDetails()
    if resetResponse['status']:
        
        message = resetResponse.get('updatedProducts','')
        print('>>>>>>',message)
        recipients = ['magezibrian108@gmail.com','receipereadalive@gmail.com'] 
        subject = 'the following products there discounts have expired and have been reset'
        mailResponse  = sendDynamicMail({'message':message,'recipients':recipients,'subject':subject,'imagePath':[]})
        return mailResponse
    return jsonify(resetResponse['log'])

@app.route('/sendDynamicMail',methods=['POST'])
def sendEmailWithAttachement():
    payload = request.get_json()
    response = sendDynamicMail(payload)
    return jsonify(response)      
# ------------------------------

def role_required(allowed_roles):
    from db import fetchRole
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({'status': False, 'log': 'Token is missing'}), 403

            try:
                # Extract the token from the 'Bearer' format
                token = token.split()[1]
            except IndexError:
                return jsonify({'status': False, 'log': 'Token format is invalid'}), 403

            try:
                # Decode the token to get user data
                data = decode_token(token, app.config['SECRET_KEY'])
                print("newdecorator>>>>>>>>>>>>>>>>>>>>",data)
                if not data:
                    return jsonify({'status': False, 'log': 'Token is invalid or expired'}), 403

                roleFetchResult = fetchRole({'roleId':data['role_id']})
                
                if roleFetchResult['status']:
                    if roleFetchResult['log'][0]['role'] not in allowed_roles:
                        return jsonify({'status': False, 'log': 'Permission denied'}), 403
                else:
                    return jsonify({'status': False, 'log': 'Permission denied'}), 403
            except:
                return jsonify({'status': False, 'log': 'Invalid token'}), 403

            # Check if the user's role is in the allowed roles
            # if user_role not in allowed_roles:
            #     return jsonify({'status': False, 'log': 'Permission denied'}), 403

            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def token_required(roles):
    from db import fetchRole
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({'status': False, 'log': 'Token is missing'}), 403

            # Extract the token from the 'Bearer' format
            try:
                token = token.split()[1]
                # print('>>>>>>>>>>>>>>>>token >>>',token)
            except IndexError:
                return jsonify({'status': False, 'log': 'Token format is invalid'}), 403

            try:
                data = decode_token(token, app.config['SECRET_KEY'])
                if not data:
                    return jsonify({'status': False, 'log': 'Token is invalid or expired'}), 403

                roleFetchResult = fetchRole({'roleId':data['role_id']})
                
                if roleFetchResult['status']:
                    if roleFetchResult['log'][0]['role'] not in roles:
                        return jsonify({'status': False, 'log': 'Permission denied'}), 403
                else:
                    return jsonify({'status': False, 'log': 'Permission denied'}), 403


                # if data['role_id'] not in roles:
                #     print('>>>>>>>>>>>>>>>>>>>>>>>>>roleId',data['role_id'])
                #     return jsonify({'status': False, 'log': 'Permission denied'}), 403

                # Attach user data to the request
                request.user = data
            except Exception as e:
                return jsonify({'status': False, 'log': 'Token is invalid'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# -----the endpoints below are responsible for logging in 
@app.route('/login', methods=['POST'])
def login():
    from db import login
    data = request.get_json()
    phoneNumber = data.get('phoneNumber')
    email = data.get('email')
    password = data.get('password')
    user = login({'phoneNumber': phoneNumber,'email':email, 'password': password})
    if user['status']:
            user_id = user['log'][0]['userId']
            role_id = user['log'][0]['roleId']
            user_name = user['log'][0]['userName']
            token = generate_token(user_id, role_id, user_name, app.config['SECRET_KEY'])
            return jsonify({'status': True,'token': token})
    
    return jsonify({'status': False, 'log': 'Invalid credentials'})
    # return render_template('login.html')



@app.route('/profile', methods=['POST'])
@token_required(['user', 'MANAGER', 'ADMIN'])
def dashboard():
    userName = request.user['user_name']
    roleId = request.user['role_id']
    from db import fetchRole
    roleList = fetchRole({'roleId':roleId})
    if roleList['status']:
        role = roleList['log'][0]['role']
        
    else:
        role = 'Unknown'
    
    return jsonify({'status': True, 'userName': userName, 'role': role})

                
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
    productinsertionresponse = insertProductIntoDb(payload)# )

    return jsonify(productinsertionresponse)

@app.route('/fetchAllProducts', methods=['POST'])

def handleFetchAllProducts():
    from db import fetchAllProducts
    '''
        This endpoint is responsible for fetching all products from the database.
    '''
    response = fetchAllProducts()
    
    return jsonify(response)

@app.route('/fetchAllProductsWithWarningStock', methods=['POST'])

def handleFetchAllProductsWithWarningStock():
    from db import fetchAllProductsWithWarningStock
    '''
        This endpoint is responsible for fetching all products with warning stock from the database.
    '''
    response = fetchAllProductsWithWarningStock()
    
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
# @checkLoggedIn()
# @checkuserRole(['MANAGER','ADMIN'])
# @loginRequired()

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

# --- the routes below are responsible for customers --------
@app.route('/registerCustomer',methods=['POST'])
def handleRegisterCustomer():
    from db import addCustomerToDb
    '''
        this endpoint is responsible for inserting/registering
         product into the database 
    '''
    payload = request.get_json()
    payload['entryId'] = kutils.codes.new()
    payload['customerId'] = kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payload['userId'] = "sirkata"
    # payload['others'] = {}
    payloadStructure = {
        'entryId':kutils.config.getValue('bmsDb/entryId'),
        'customerId':kutils.config.getValue('bmsDb/customerId'),
        'timestamp':kutils.config.getValue('bmsDb/timestamp'),
        'customerName':kutils.config.getValue('bmsDb/customerName'),
        'customerPhoneNumber':kutils.config.getValue('bmsDb/customerPhoneNumber'),
        'customerLocation':kutils.config.getValue('bmsDb/customerLocation'),
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
    productinsertionresponse = addCustomerToDb(payload)
    return jsonify(productinsertionresponse)

@app.route('/fetchAllCustomers', methods=['POST'])
# @checkLoggedIn()
# @checkuserRole(['MANAGER','ADMIN'])
def handleFetchAllCustomers():
    from db import fetchAllCustomers
    '''
        This endpoint is responsible for fetching all products from the database.
    '''
    response = fetchAllCustomers()
    
    return jsonify(response)

@app.route('/fetchSpecificCustomer', methods=['POST'])
def handleFetchSpecificCustomer():
    from db import fetchCustomerById
    '''
        This endpoint is responsible for fetching a specific product from the database.
    '''
    payload = request.get_json()
    productDetails = {
        'customerId': payload.get('customerId')
    }
    
    if not productDetails['productName'] :
        return jsonify({'status': False, 'log': 'Product name and serial number are required'}), 400

    response = fetchCustomerById(productDetails)
    
    return jsonify(response)


# --- the routes below are responsible for handling database operations of sales
'''
    this module is responsible for handling routes for the sales module 
    these include these include fetching,editing,deleting and adding
'''
@app.route('/addSale', methods=['POST'])
@token_required(['ADMIN','user','MANAGER'])
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
    payload['others'] = {'userName':request.user['user_name']}
    payload['soldBy'] = request.user['user_name']

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
        print('credit',addCreditDetailsResponse)
        return {'status':True,'log':'sale added successfully','saleId':payload['saleId']}
    
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
    
    # if not saleDetails['saleDate']:
    #     return jsonify({'status': False, 'log': 'Sale Date are required'}), 400

    response = fetchSpecificSalesFromTo(saleDetails)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>date from to ',response)
    
    return jsonify(response)

@app.route('/addSingleProductSale', methods=['POST'])
@token_required(['ADMIN','user','MANAGER'])

def handleAddSingleProductSale():
    '''
    This endpoint is responsible for adding individual product sales to the database.
    '''
    from db import addSingleProductSale
    
    
    payload = request.get_json()
    print('Received payload:', payload)  # Debug: Print received payload

    if not payload:
        return jsonify({'status': False, 'log': 'No data provided'}), 400
    
    # Assuming payload is a list of single product sales
    print('>>>>>>singlepdtsalepayload',payload)
    for productSale in payload:
        productSale['entryId'] = kutils.codes.new()
        productSale['timestamp'] = kutils.dates.currentTimestamp()
        productSale['dateSold'] = kutils.dates.today()
        productSale['others'] = {'soldBy':request.user['user_name']}
    
    print('Payload after adding entryId and timestamp:', productSale['others'])  # Debug: Print modified payload
    
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

@app.route('/adduser',methods=['POST'])
@role_required(['MANAGER'])
def handleAdduser():
    '''
    this function is responsible for handling 
    the adduser endpoint 
    '''
    from db import createuser
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
        
        createuserResponse  = createuser(payload)
        
        if not createuserResponse['status']:
            return jsonify(createuserResponse)
    
    return jsonify(validationResponse)

@app.route('/fetchAllusers',methods=['POST'])
def handleFetchAllusers():
    from db import fetchAllusers
    
    response = fetchAllusers()
    return jsonify(response)

@app.route('/resetPassword',methods=['POST'])
def handleResetPassword():
    '''
        this endpoint is responsible for handling 
        resetting users password the expected key in the 
        payload is 'phoneNumber'
    '''
    from db import resetuserPassword
    payload = request.get_json()
    payloadStructure = {
        'phoneNumber':kutils.config.getValue('bmsDb/phoneNumber')
    }
    payloadValidationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    if payloadValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({'status':False,'log':f"the value for {key} is missing please provide it "})
        response = resetuserPassword(payload)
        return jsonify(response) 
    return jsonify(payloadValidationResponse)

# -------module for credit endpoints-----------

@app.route('/fetchAllCredits',methods=['POST'])

def handleFetchAllCredits():
    from db import fetchAllCredits
    
    response = fetchAllCredits()
    return jsonify(response)

@app.route('/fetchAllUnclearedCredits',methods=['POST'])

def handleFetchAllUnclearedCredits():
    from db import fetchAllUnClearedCredits
    
    response = fetchAllUnClearedCredits()
    return jsonify(response)


@app.route('/editCredit',methods = ['POST'])
def handleEditCredit():
    from db import editCredit
    payload = request.get_json()
    print('....payload recieved',payload)
    payloadStructure = {
        
        'amountPaid':kutils.config.getValue('bmsDb/amountPaid'),
        'saleId':kutils.config.getValue('bmsDb/saleId'),
        'creditId':kutils.config.getValue('bmsDb/creditId'),
        'paymentStatus':kutils.config.getValue('bmsDb/paymentStatus'),
        
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
@role_required(['ADMIN'])
def handleCreateRole():
    
    '''
        this endpoint is responsible for creating a a role 
        
    '''
    from db import createRoles
    payload = request.get_json()
    # payload['entryId'] = kutils.codes.new()
    # payload['roleId'] = kutils.codes.new()
    # payload['timestamp'] = kutils.dates.currentTimestamp()
    payloadStructure = {
        # 'entryId':kutils.config.getValue('bmsDb/entryId'),
        # 'timestamp':kutils.config.getValue('bmsDb/timestamp'),
        # 'roleId':kutils.config.getValue('bmsDb/roleId'),
        'role':kutils.config.getValue('bmsDb/role'),
        'others':kutils.config.getValue('bmsDb/others')
       
    }
    print('>>>>>>>>>>>>creating a role',payload)
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
# -----this module is responsible for handling all unit related end points
@app.route('/createUnit',methods=['POST'])
@token_required(['ADMIN','MANAGER'])
def handleCreateUnit():
    '''
        this endpoint is responsible for creating a a role 
        
    '''
    from db import createUnit
    payload = request.get_json()
    payload['entryId'] = kutils.codes.new()
    payload['unitId'] = kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payload['others'] = {'registeredBy':request.user['user_name']}
    payloadStructure = {
        'entryId':kutils.config.getValue('bmsDb/entryId'),
        'timestamp':kutils.config.getValue('bmsDb/timestamp'),
        'unitId':kutils.config.getValue('bmsDb/unitId'),
        'unit':kutils.config.getValue('bmsDb/unit'),
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
        
        print('>>>>>>>fromFrontend createUnit',payload)
        createRoleResponse  = createUnit(payload)
        
        if not createRoleResponse['status']:
            return jsonify(createRoleResponse)
    
    return jsonify(validationResponse)

@app.route('/fetchAllUnits',methods=['POST'])
def handleFetchAllUnits():
    from db import fetchAllUnits
    
    response = fetchAllUnits()
    return jsonify(response)

@app.route('/fetchUnit',methods=['POST'])
def handleFetchUnit():
    from db import fetchUnit
    payload = request.get_json()
    payloadStructure = {
        'unitId':kutils.config.getValue('bmsDb/unitId'),
    }
    validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if validationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
        
        createRoleResponse  = fetchUnit(payload)
        
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
    # payload['entryId'] = kutils.codes.new()
    # payload['categoryId'] = kutils.codes.new()
    # payload['timestamp'] = kutils.dates.currentTimestamp()
    payloadStructure = {
        # 'entryId':kutils.config.getValue('bmsDb/entryId'),
        # 'timestamp':kutils.config.getValue('bmsDb/timestamp'),
        # 'categoryId':kutils.config.getValue('bmsDb/categoryId'),
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
        print('>>>>>>>>>>>>>>>>>>>from frontend',payload)
        createRoleResponse  = addCategoryToDb(payload)
        
        if not createRoleResponse['status']:
            return jsonify(createRoleResponse)
    
    return jsonify(validationResponse)


# ------ the following endPoints below are responsible handling expenses ----------

@app.route('/createAnExpense',methods=['POST'])
def createExpense():
    '''
        the following endPoint is responsible for handling adding of an expense to the database 
        @param: the following are the expected keys in the in the payload
                'entryId','dateOfExpense','timestamp','dateOfExpense','description','amountSpent'
    '''
    from db import addExpenseToDb
    payload = request.get_json()
    payload['entryId'] = kutils.codes.new()
    payload['dateOfExpense'] = kutils.dates.today()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payloadStructure = {
        'entryId':kutils.config.getValue('bmsDb/entryId'),
        'timestamp':kutils.config.getValue('bmsDb/timestamp'),
        'description':kutils.config.getValue('bmsDb/description'),
        'dateOfExpense':kutils.config.getValue('bmsDb/dateOfExpense'),
        'amountSpent':kutils.config.getValue('bmsDb/amountSpent'),
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
        
        createRoleResponse  = addExpenseToDb(payload)
        
        if not createRoleResponse['status']:
            return jsonify(createRoleResponse)
    
    return jsonify(validationResponse)

@app.route('/fetchAllExpense',methods=['POST'])
def handleFetchExpenses():
    from db import fetchExpensesFromDb
    
    expensesFetchResponse = fetchExpensesFromDb()
    
    return jsonify(expensesFetchResponse)

@app.route('/fetchSpecificDateExpenses',methods=['POST'])
def handleSpecificDateExpenses():
    from db import fetchSpecificExpenseByDate
    payload = request.get_json()
    
    payloadStructure = {
        'dateOfExpense':kutils.config.getValue('bmsDb/dateOfExpense')
    }
    
    payloadValidationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    if not payloadValidationResponse('status'):
        return jsonify(payloadValidationResponse)
    for key in payload:
        if not payload['key']:
            return jsonify({
                'status':False,
                'log':f'the value of {key} is missing please provide it '
            })
    expenseFetchResponse = fetchSpecificExpenseByDate(payload)
    return jsonify(expenseFetchResponse)
    
@app.route('/fetchExpensesFromTo',methods=['POST'])
def handleFetchSpecificExpensesFromTO():
    '''
        this end point is responsible for fetching expenses 
        from and to a specific date 
    '''
    from db import fetchSpecificExpensesFromTo
    payload = request.get_json()
    payloadStructure = {
        'dateFrom':kutils.config.getValue('bmsDb/dateFrom'),
        'dateTo':kutils.config.getValue('bmsDb/dateTo')
    }
    
    payloadValidationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if payloadValidationResponse['status']:
        for key in payload:
            if not payload['key']:
                return jsonify({
                    'status':False,
                    'log':f'the value of {key} is missing please provide it'
                })
        fetchSpecificExpenseResponse = fetchSpecificExpensesFromTo(payload)
        return jsonify(fetchSpecificExpenseResponse)
    return jsonify (payloadValidationResponse)
    
# --- the endpoints below are responsible for generation of reports ----
@app.route('/fetchAllSalesReports', methods=['POST'])
def fetch_all_sales():
    from db import fetch_sales_with_pagination
    limit = 100
    page = request.json.get('page', 1)
    response = fetch_sales_with_pagination(limit, page)
    return jsonify(response)

@app.route('/fetchSpecificSalesReports', methods=['POST'])
def fetchSpecificSalesReports():
    from db import fetchSpecificSaleReport
    payload = request.get_json()
    saleDetails = {
        'saleDate': payload.get('saleDate'),
        
    }
    if not saleDetails['saleDate']:
        return jsonify({'status': False, 'log': 'Sale Date are required'}), 400
    limit = 100
    page = request.json.get('page', 1)
    response = fetchSpecificSaleReport(limit, page,saleDetails)
    return jsonify(response)

@app.route('/fetchSpecificSalesFromToReports', methods=['POST'])
def fetchSpecificSalesFromToReports():
    from db import fetchSpecificSalesFromToReports
    payload = request.get_json()
    saleDetails = {
        'dateTo': payload.get('dateTo'),
        'dateFrom':payload.get('dateFrom')
        
    }
    # if not saleDetails['saleDate']:
    #     return jsonify({'status': False, 'log': 'Sale Date are required'}), 400
    limit = 100
    page = request.json.get('page', 1)
    response = fetchSpecificSalesFromToReports(limit, page,saleDetails)
    return jsonify(response)

@app.route('/revokeuser',methods=['POST'])
@token_required(['ADMIN','MANAGER'])
def revokeuserPermissions():
    '''
        this  endpoint is responsible for revoking user permissions 
    '''
    print('>>>>>>>>>username',request.user['user_name'])
    from db import revokeuser
    payload = request.get_json()
    payload['other'] = {"revokedBy":request.user['user_name'],"revokerId":request.user['user_id']}
    print('>>>>>>',payload)
    payloadStructure = {
        'phoneNumber':kutils.config.getValue('bmsDb/phoneNumber'),
        'other':kutils.config.getValue('bmsDb/other')
    }
    payloadStructureValidationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    if payloadStructureValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return{
                    'status':False,
                    'log':f"The value for {key} is missing please provide it "
                }
            response = revokeuser(payload)
            return jsonify(response)     
    return payloadStructureValidationResponse

# ----the endPoints below handle discount ----
@app.route('/setProductDiscount',methods=['POST'])
def setProductDiscount():
    '''
    this endPoint is responsible for for setting product discounts 
    the following are keys are expected to be in the payload 
    'productId','discountRate','expiryDate'
    '''
    from db import setProductDiscountPrice
    payload = request.get_json()
    payloadStructure = {
        'productIds':kutils.config.getValue('bmsDb/productIds'),
        'discountRate':kutils.config.getValue('bmsDb/discountRate'),
        'expiryDate':kutils.config.getValue('bmsDb/expiryDate')
    }
    payloadValidationResponse  = kutils.structures.validator.validate(payload,payloadStructure)
    
    if payloadValidationResponse['status']:
        for key in  payload:
            if not payload[key]:
                return jsonify({'status':False,'log':f'the value of {key} is missing please provide it'})
        response = setProductDiscountPrice(payload)
        return jsonify(response)
    return jsonify(payloadValidationResponse) 

@app.route('/setProductFlatDiscount',methods=['POST'])
def setProductFlatDiscount():
    '''
    this endPoint is responsible for for setting product discounts 
    the following are keys are expected to be in the payload 
    'productId','discountRate','expiryDate'
    '''
    from db import setProductFlatDiscountPrice
    payload = request.get_json()
    payloadStructure = {
        'productIds':kutils.config.getValue('bmsDb/productIds'),
        'discountRate':kutils.config.getValue('bmsDb/discountRate'),
        'expiryDate':kutils.config.getValue('bmsDb/expiryDate')
    }
    payloadValidationResponse  = kutils.structures.validator.validate(payload,payloadStructure)
    
    if payloadValidationResponse['status']:
        for key in  payload:
            if not payload[key]:
                return jsonify({'status':False,'log':f'the value of {key} is missing please provide it'})
        response = setProductFlatDiscountPrice(payload)
        return jsonify(response)
    return jsonify(payloadValidationResponse) 

@app.route('/setFlatSaleDiscount',methods=['POST'])
def setFlatSaleDiscount():
    '''
    this endPoint is responsible for for flatSale discounts 
    the following are keys are expected to be in the payload 
    'grandTotal','discountRate'
    '''
    from db import setFlatSaleDiscount
    payload = request.get_json()
    payloadStructure = {
        'grandTotal':kutils.config.getValue('bmsDb/grandTotal'),
        'discountRate':kutils.config.getValue('bmsDb/discountRate'),
        'weightAmount':kutils.config.getValue('bmsDb/weightAmount')
    }
    payloadValidationResponse  = kutils.structures.validator.validate(payload,payloadStructure)
    
    if payloadValidationResponse['status']:
        for key in  payload:
            if not payload[key]:
                return jsonify({'status':False,'log':f'the value of {key} is missing please provide it'})
        response = setFlatSaleDiscount(payload)
        return jsonify(response)
    return jsonify(payloadValidationResponse) 


@app.route('/setTieredDiscount', methods=['POST'])
def set_tiered_discount():
    """
    This endpoint handles tiered discounts based on the total sale amount.
    The following keys are expected in the payload:
        - 'totalAmount': The total sale amount (float).
        - 'tiers': A list of tuples [(min_amount, discount_rate)].
    """
    from db import setTieredDiscount                                                                                                                                                                                                                                                                                                                                                                        
    try:
        # Get the JSON payload from the request
        payload = request.get_json()

        # Check if the required keys exist and have the correct types
        if 'totalAmount' not in payload or not isinstance(payload['totalAmount'], (int, float)):
            return jsonify({
                'status': False,
                'log': 'The key "totalAmount" is missing or invalid. Expected a number.'
            }), 400

        if 'tiers' not in payload or not isinstance(payload['tiers'], list):
            return jsonify({
                'status': False,
                'log': 'The key "tiers" is missing or invalid. Expected a list.'
            }), 400

        # Validate the format of the tiers
        for tier in payload['tiers']:
            if not isinstance(tier, list) or len(tier) != 2:
                return jsonify({
                    'status': False,
                    'log': 'Invalid format for "tiers". Expected a list of lists [(min_amount, discount_rate)].'
                }), 400

        # Process the tiered discount using the setTieredDiscount function
        response = setTieredDiscount(payload)

        return jsonify(response), 200

    except Exception as e:
        # Return error response in case of an exception
        return jsonify({
            'status': False,
            'log': f'An error occurred: {str(e)}'
        }), 500

@app.route('/fetchAllDiscountedProducts', methods=['POST'])
# @checkuserRole(['MANAGER','ADMIN'])
def handleFetchAllDiscountedProducts():
    from db import fetchAllProductsWithDiscount
    '''
        This endpoint is responsible for fetching all products from the database.
    '''
    response = fetchAllProductsWithDiscount()
    
    return jsonify(response)
# ----the following endpoints below are responsible for handling the business documents  module ----
@app.route('/generateInvoice', methods=['POST'])
def handleGenerateInvoice():
    data = request.get_json()
    from db import fetchAllProducts

    customer = data.get('customer')
    products = data.get('products')

    if not customer or not products:
        return jsonify({'status': False, 'log': 'Customer and products are required'})

    total_price = 0
    invoice_items = []

    all_products = fetchAllProducts()
    if not all_products.get('status'):
        return jsonify({'status': False, 'log': 'Failed to fetch products from database'})

    product_list = all_products.get('log', [])

    for product in products:
        product_id = product.get('productId')
        quantity = int(product.get('quantity', 0))

        product_details = next((p for p in product_list if p['productId'] == product_id), None)
        if not product_details:
            return jsonify({'status': False, 'log': f'Product with ID {product_id} not found'})

        sale_price = product_details.get('productSalePrice')
        if sale_price is None:
            return jsonify({'status': False, 'log': f'Product ID {product_id} has no sale price'})

        item_total = sale_price * quantity
        total_price += item_total

        invoice_items.append([
            product_id,
            product_details.get('productName'),
            quantity,
            sale_price,
            item_total
        ])

    # Generate Invoice as Excel File
    invoice_file = generate_excel_invoice(customer, invoice_items, total_price)

    return send_file(invoice_file, as_attachment=True, download_name="Invoice.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def generate_excel_invoice(customer, items, total_price):
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice"

    # Header
    ws.append(["Invoice", "", "", "", ""])
    ws.append(["Customer", customer, "", "", ""])
    ws.append(["Date", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "", "", ""])
    ws.append(["", "", "", "", ""])
    ws.append(["Product ID", "Product Name", "Quantity", "Sale Price", "Total Price"])

    # Invoice Items
    for item in items:
        ws.append(item)

    # Footer
    ws.append(["", "", "", "Grand Total:", total_price])

    # Save the file in a temporary directory
    invoice_path = f"invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    wb.save(invoice_path)

    return invoice_path


def init():
    
        defaults = {
            'recipients':list,
            'message':str,
            'subject':str,
            'tiers':list,
            'weightAmount':int,
            'productIds':list,
            'discountRate':str,
            'expiryDate':str,
            'dateFrom':str,
            'dateTo':str,
            'dateOfExpense':str,
            'description':str,
            'amountSpent':int,
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
            'other':dict,
            'saleId':str,
            'unit':str,
            'unitId':str,
            'customerName':str,
            'customerPhoneNumber':str,
            'customerId':str,
            'customerLocation':str,
            'amountInDebt':int,
            'SECRETE_KEY':kutils.codes.new(),
            'SESSION_TYPE':'filesystem',
            'SESSION_PERMANENT':False,
            'SESSION_user_SIGNER':True,
            'email':'adamzhakeam@gmail.com',
            'mailPassword':'xzhf bphb kwuz ybzj'
            
        }
        config_topic = 'bmsDb'
        
        for key in defaults:
            if 1 or not kutils.config.getValue(config_topic+'/'+key):
                kutils.config.setValue(config_topic+'/'+key,defaults[key])
                
init()

if __name__ == "__main__":
     app.run(debug=True,host = '0.0.0.0',port = 5000)
    #  app.run(debug=True,host = '0.0.0.0',port = 8080)