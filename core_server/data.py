import requests
for i in range(40):
    url = "http://10.44.15.94:8000/olps/transact"
    body = {
	"rfid":{
    "rfid_value": "50b668139b770cef254f75596a236bae27cf0a3c",
    "label": "First label",
    "is_enabled": "false",
    "disability_reason": "None"
},
	"pos":{	
    "api_key": "0ee651b9b3a93a9f1e2e758781e60b98e7fd35bf",
    "label": "First pos",
    "is_enabled": "true"
},
	"amount":10,
	"lat":18.9247995,
	"lan":72.8188888
}
    headers = {
    "authkey":"199192AN8u9SKkpL5a8d8d97",
        "Content-Type":"application/json"
    }
    r = requests.post(url,json=body,headers=headers)
    
    print(r.json())