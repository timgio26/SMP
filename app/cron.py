import requests
import json
from base64 import b64encode
import config

### API WEB APP
def getcred():
    setup = requests.get("{0}/apiv1?data=credentials&secretkey={1}".format(config.envurl,config.SECRET_KEY))
    return(setup.json()[0])

def getprod():
    prod = requests.get("{0}/apiv1?data=product".format(config.envurl))
    prodlist=[int(x['product_id']) for x in prod.json()]
    return(prodlist)

def getwh():
    wh = requests.get("{}/apiv1".format(config.envurl))
    whlist=[int(x['warehouse_id']) for x in wh.json()]
    return(whlist)

def addstok(prodid,stokval,whid):
    r = requests.post("{0}/apiv1?id={1}&qty={2}&wh={3}".format(config.envurl,prodid,stokval,whid))
    return(r.json())

def newtoken(newtoken):
    r = requests.post("{0}/apiv1?data={1}&secretkey={2}&newtoken={3}".format(config.envurl,'token',config.SECRET_KEY,newtoken))
    return(r.json())

### External API
def getip():
    return(requests.get("https://api.ipify.org?format=json").json()["ip"])

### Tokopedia API
def gettoken(id,secret):
    reqcred="{0}:{1}".format(id,secret)
    credentials = b64encode(bytes(reqcred, encoding='utf-8'))
    r = requests.post("https://accounts.tokopedia.com/token?grant_type=client_credentials",
                    headers={"Authorization": "Basic " + credentials.decode("utf-8")})
    return(r.json()['access_token'])

def getstoreinfo(fs_id,token):
    url="https://fs.tokopedia.net/v1/shop/fs/{0}/shop-info".format(fs_id)
    r = requests.get(url,headers={"Authorization": "Bearer " + token})
    return(r.json())

def getprodinfo(fs_id,itemid,token):
    url='https://fs.tokopedia.net/inventory/v1/fs/{0}/product/info?product_id={1}'.format(fs_id,itemid)
    r = requests.get(url,headers={"Authorization": "Bearer " + token})
    return(r.json())

cred=getcred()
wh=getwh()
for itemid in getprod():
    print("=====================")
    print(itemid)
    prodinfo=getprodinfo(cred['appId'],itemid,cred['clientBearer'])
    if 'message' in prodinfo.keys():
        if prodinfo['message']=='invalid_token':
            tokenbaru=gettoken(id=cred['clientId'],secret=cred['clientSecret'])
            newtoken(newtoken=tokenbaru)
        elif prodinfo['message']=='unauthorized_ip_address':
            currentip=requests.get("https://api.ipify.org?format=json").json()["ip"]
            print('please register IP: {}'.format(currentip))
            break
        else:
            print('check error msg')
            break
        cred=getcred()
        prodinfo=getprodinfo(cred['appId'],itemid,cred['clientBearer'])
    for i in prodinfo['data'][0]['warehouses']:
        if i['warehouseID'] in wh:
            if 'value' in i['stock']:
                addstok(prodid=itemid,stokval=i['stock']['value'],whid=i['warehouseID'])
                print('{0}:{1}'.format(i['warehouseID'],i['stock']['value']))
            else:
                addstok(prodid=itemid,stokval=0,whid=i['warehouseID'])
                print('{0}:{1}'.format(i['warehouseID'],0))
        else:
            print('unregistered wh: {}'.format(i['warehouseID']))