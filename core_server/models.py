from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class EndUser(models.Model):
    acc_no=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32,null=False)
    balance=models.IntegerField()
    phone_no=models.CharField(max_length=13,null=False,default="100" )
    django_user=models.ForeignKey(User,unique=True,on_delete=models.CASCADE)
    
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
    disability_reason=models.CharField(max_length=32,default='None')
    user=models.ForeignKey(EndUser,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return '%s:%s'%(self.user,self.label)

    class Meta:
        ordering=['rfid']

class Transaction(models.Model):
    transaction_id=models.AutoField(primary_key=True)
    amount=models.IntegerField(null=False,default=0)
    txn_status=models.CharField(null=False,max_length=7,
        choices=(
            ("success", "SUCCESS"),
            ("failed", "FAIL"),
            ("pending", "PENDING")))
    lat=models.FloatField(default=0)
    lan=models.FloatField(default=0)

    user=models.ForeignKey(EndUser,on_delete=models.CASCADE,null=True,related_name="User")
    vendor=models.ForeignKey(EndUser,on_delete=models.CASCADE,null=True,related_name="Vendor")
    RFID=models.ForeignKey(RFID,on_delete=models.CASCADE,null=True)
    PoS=models.ForeignKey(PoS,on_delete=models.CASCADE,null=True)
	
	
