'''
    this module is responsible for creating e-tickets with a qr code 
    
'''
import qrcode
import kisa_utils as kutils
import hashlib
from bms.app import sendDynamicMail
def generateQrCode(clientDetails:dict)->dict:
    '''
        this function is responsible for generating a qr code 
        with client details
        @param clientDetails: 'clientName','email','phoneNumber', 
    '''
    from db import insertTicketIntoDb
    data = generate(clientDetails)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='red', back_color='white')
    ticketId , ticket = data.split('|')
    if insertTicketIntoDb({'ticketId':ticketId,'ticket':ticket})['status']:
        
        # /home/predator/Documents/hbms/bms/static/images/logo-color (1).png
        imagePath = f"/home/predator/Documents/hbms/bms/static/images/EroticHousePartyQr.png"
        img.save(imagePath)
        return imagePath
    return {'status':False, 'log':'failed to generate and save ticket'}    

def generate(clientDetails:dict)->dict:
    '''
        this function is responsible for generating a qr code 
        with client details
        @param clientDetails: 'clientName','email','phoneNumber','ticketId' 
    '''
    ticketId = 'ticketId'+kutils.codes.new()
    data = f"{clientDetails['clientName']}|{clientDetails['email']}|{clientDetails['phoneNumber']}|{ticketId}"
    hashData = hashlib.sha256(data.encode()).hexdigest()
    return f"{ticketId}|{hashData}"

def verifyTicket(ticketDetails:dict)->dict:
    '''
        this function is responsible for verifying the ticket
        @param ticketDetails:'ticketId' is a required key
    '''
    from db import fetchTicketById,setVerificationStatus
    response = fetchTicketById({'ticketId':ticketDetails['ticketId']})
    if response['status']:
        updateStatus = setVerificationStatus({'ticketId':ticketDetails['ticketId']})
        if updateStatus:
            return {'status':True,'log':'verification successful'}
        return updateStatus
    return response 
        
if __name__ =='__main__':
    # print(generateQrCode('adamzKata'))
    mail = {
        "recipients":["magezibrian108@gmail.com"],
        "message":"testing attachments",
        "subject":"e-ticket",
        "imagePath":["/home/predator/Documents/hbms/bms/ticket_adamzKata.png"]
    }
    
    clientData = {
        "clientName":"quinxella",
        "email":"quinxella@gmail.com",
        "phoneNumber":"0776345543",
        "clientId":kutils.codes.new()
        
    }
    print(generateQrCode(clientData))
    # print(sendDynamicMail(mail))