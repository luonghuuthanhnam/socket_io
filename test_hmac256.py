import hmac
import hashlib
import json
import time
import requests
URL = "https://test-payment.momo.vn/gw_payment/transactionProcessor"


from datetime import datetime

def get_time():
    today = datetime.today()
    today.timestamp()
    str_today = str(today)
    str_today = str_today.replace('-','')
    str_today = str_today.replace(':','')
    str_today = str_today.replace('.','')
    str_today = str_today.replace(' ','')
    return str_today

secr = "pdxnHUEXWFeC53AE5ZSyFAmrkvXCJsf2"
endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"

data = {}
data['accessKey'] = "StAb3COtTvgYFlSQ"
data['partnerCode'] = "MOMOTAQ220190330"
data['requestType'] = "captureMoMoWallet"
data['notifyUrl'] = "https://openlab.hcmute.edu.vn"
data['returnUrl'] = "https://openlab.hcmute.edu.vn"
data['orderId'] = "150000"
data['amount'] = "150000"
data['orderInfo'] = "Hello World"
data['requestId'] = "MM001"
data['extraData'] = "email=luonghuuthanhnam5@gmail.com"
data['signature'] = "73629a868b81b527564b310bddce3bc23a5339ea574f6c3c502ccb5aa6bffe3f"

orderID = ""
requestID = ""

def check_status():
    global data
    data_check = {}
    data_check['partnerCode']=data['partnerCode']
    data_check['accessKey'] = data['accessKey']
    data_check['requestId'] = data['requestId']
    data_check['orderId'] = data['orderId']
    data_check['requestType'] = "transactionStatus"

    prsig = "partnerCode=" + data_check['partnerCode'] + "&accessKey=" + data_check['accessKey'] + "&requestId=" + data_check['requestId'] + "&orderId=" + data_check['orderId'] + "&requestType=" + data_check['requestType']
    _sig = hmac.new(bytes(secr , 'latin-1'), msg = bytes(prsig , 'latin-1'), digestmod = hashlib.sha256).hexdigest()
    data_check['signature'] = _sig



    r1 = requests.post(URL, json.dumps(data_check))
    data_reponse1 = r1.json()
    print(data_reponse1['localMessage'])
    #print(data_check['signature'])


def make_pre_sig():
    global data
    return "partnerCode=" + data['partnerCode'] + "&accessKey=" + data['accessKey'] + "&requestId=" + data['requestId'] + "&amount=" + data['amount'] + "&orderId=" + data['orderId'] + "&orderInfo=" + data['orderInfo'] + "&returnUrl=" + data['returnUrl'] + "&notifyUrl=" + data['notifyUrl'] + "&extraData=" + data['extraData']

def get_signature(_amount, order_infor):
    global requestId, amount, orderInfo, orderId, data
    time_id = get_time()
    requestId = time_id + "request_id"
    amount = _amount
    orderId = time_id + "order_id"
    orderInfo = order_infor

    data['orderId'] = orderId
    data['requestId'] = requestId
    data['amount'] = amount
    data['orderInfo'] = orderInfo

    presig = make_pre_sig()
    sig = hmac.new(bytes(secr , 'latin-1'), msg = bytes(presig , 'latin-1'), digestmod = hashlib.sha256).hexdigest()
    data['signature'] = sig
    #print (sig)
    return sig
res_sig = ""
qr_url = ""
def get_reponse():
    global res_sig, qr_url
    get_signature("100000","vien phi")
    r = requests.post(URL, json.dumps(data))
    data_reponse = r.json()
    res_sig = data_reponse['signature']
    print(data_reponse)

get_reponse()
while 1:
    check_status()
    time.sleep(1)

