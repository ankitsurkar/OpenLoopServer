from .models import SpendingRules, EndUser
import time
import hashlib
import requests
def ValidateSpendingRule(enduser, amount):
    spending_rule = SpendingRules.objects.get(user = enduser)
    if spending_rule.enable_next_txn:
        spending_rule.enable_next_txn = False
        spending_rule.save()
        return True

    if (time.time() - spending_rule.start_time) > spending_rule.reset_period:
        spending_rule.total_txn_amt = 0
        spending_rule.txn_no = 0
        spending_rule.start_time  = time.time()
        spending_rule.save()

    if (spending_rule.txn_no == spending_rule.txn_no_limit) or (spending_rule.total_txn_amt + amount > spending_rule.total_txn_amt_limit) or (amount > spending_rule.per_txn_amt_limit):
        spending_rule.secret_no = hashlib.sha1(str(enduser.django_user.password+str(time.time())).encode('utf-8')).hexdigest()
        spending_rule.save()
        SendLink(spending_rule.secret_no,enduser)
        return False
    else:
        spending_rule.txn_no = spending_rule.txn_no + 1
        spending_rule.total_txn_amt = spending_rule.total_txn_amt + amount
        spending_rule.save()
        return True        

def SendLink(secret_no,enduser):
    url = "http://api.msg91.com/api/v2/sendsms"
    
    message = "[Team Falcons]Click the following link to enable the next transaction:http://10.44.15.94:8000/olps/en/"+secret_no
    body = {
        "sender":"OPLOOP",
        "route":4,
        "country":91,
        "sms":[{
            "message":message,
            "to":[enduser.phone_no]
        }]
    }
    headers={
        "authkey":"199192AN8u9SKkpL5a8d8d97",
        "Content-Type":"application/json"
    }
    r = requests.post(url,json=body,headers=headers)
    
    print(r.json())
    return 