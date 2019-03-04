from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class EndUser(models.Model):
    acc_no=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32,null=False)
    balance=models.IntegerField()
    django_user=models.ForeignKey(User,unique=True,on_delete=models.CASCADE)

    def __str__(self):
        return '%s:%s'%(self.acc_no,self.name)

    class Meta:
        ordering=['acc_no']

class Vendor(models.Model):
    vendor_no=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32,null=False)
    balance=models.IntegerField()
    django_user=models.ForeignKey(User,unique=True,on_delete=models.CASCADE)
    accept_deffered_payments=models.BooleanField(default=False)


    def __str__(self):
        return '%s:%s'%(self.vendor_no,self.name)

    class Meta:
        ordering=['vendor_no']

class PoS(models.Model):
    pos_id=models.AutoField(primary_key=True)
    api_key=models.CharField(max_length=12,null=False,blank=False)
    label=models.CharField(max_length=32,null=False)
    is_enabled=models.BooleanField(default=True)

    vendor=models.ForeignKey('Vendor',on_delete=models.CASCADE,null=False)

    def __str__(self):
        return '%s:%s'%(self.pos_id,self.label)

    class Meta:
        ordering=['pos_id']

	
	
