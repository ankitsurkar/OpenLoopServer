from django.db import models
from django.contrib.auth.models import User
import time

transaction_status = {0: "Successfull", 1: "Initiated", 2: "RFID disabled", 3: "PoS disabled", 4: "Insufficient balance"}
SUCCESS = 0
INITIATED = 1
RFID_DISABLED = 2
POS_DISABLED = 3
INSUF_BALANCE = 4
# Create your models here.
class EndUser(models.Model):
    acc_no=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32,null=False)
    balance=models.IntegerField()
    phone_no=models.CharField(max_length=13,null=False,default="100" )
    django_user=models.ForeignKey(User,unique=True,on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False, null=False)
    token = models.CharField(max_length = 128, null = True, default = None)
    
    def __str__(self):
        return '%s:%s'%(self.acc_no,self.name)

    class Meta:
        ordering=['acc_no']

class PoS(models.Model):
    pos_id=models.AutoField(primary_key=True)
    api_key=models.CharField(max_length=128,null=False,blank=False)
    label=models.CharField(max_length=32,null=False)
    is_enabled=models.BooleanField(default=True)

    vendor=models.ForeignKey(EndUser,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return '%s:%s'%(self.pos_id,self.label)

    class Meta:
        ordering=['pos_id']

class RFID(models.Model):
    rfid=models.AutoField(primary_key=True)
    rfid_value=models.CharField(max_length=128,null=False,blank=False)
    label=models.CharField(max_length=32,null=False)
    is_enabled=models.BooleanField(default=True)
    pending_write=models.BooleanField(default=True)
    disability_reason=models.CharField(max_length=32,default='None')
    user=models.ForeignKey(EndUser,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return '%s:%s'%(self.user,self.label)

    class Meta:
        ordering=['rfid']

class Transaction(models.Model):
    transaction_id=models.AutoField(primary_key=True)
    amount=models.IntegerField(null=False,default=0)
    txn_status=models.CharField(null=False,max_length=32, default = transaction_status[INITIATED])
    lat=models.FloatField(default=0)
    lan=models.FloatField(default=0)
    timestamp=models.DateTimeField(null=False,auto_now=True)
    #This is the txn that will be shown to user
    txn_id = models.CharField(max_length = 128, default = "NA")
    rfid=models.ForeignKey(RFID,on_delete=models.CASCADE,null=True)
    pos=models.ForeignKey(PoS,on_delete=models.CASCADE,null=True)
	
class SpendingRules(models.Model):
    enable_next_txn = models.BooleanField(default=False)
    secret_no = models.CharField(max_length=128,default=None, null=True)
    per_txn_amt_limit = models.IntegerField(default=100)
    total_txn_amt_limit = models.IntegerField(default=300)
    txn_no_limit = models.IntegerField(default=15)
    reset_period = models.IntegerField(default=24 * 3600)
    start_time = models.IntegerField(default=time.time())

    total_txn_amt = models.IntegerField(default=0)
    txn_no = models.IntegerField(default=0)

    user = models.OneToOneField(EndUser,on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s'%(self.user.name,self.txn_no)
