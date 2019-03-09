from rest_framework import serializers
from .models import SpendingRules
import time

class DjangoUser(serializers.Serializer):
    password = serializers.CharField(max_length = 32, required = True)
    username = serializers.CharField(max_length = 32, required = True) 

class EndUserSerializer(serializers.Serializer):
    name = serializers.CharField( max_length = 32, required = True)
    django_user = DjangoUser()
    phone_no = serializers.CharField(max_length = 13,required=True)
    is_vendor = serializers.BooleanField(required=True)
    token = serializers.CharField(max_length = 128, required = False)
    balance = serializers.IntegerField(required = False)


class RFIDSerializer(serializers.Serializer):
    rfid_value = serializers.CharField(max_length = 128,required = True)
    label = serializers.CharField(max_length = 32, required = False, default = "Default label")
    is_enabled = serializers.BooleanField(required = False)
    disability_reason = serializers.CharField(max_length = 32, required = False)

class PoSSerializer(serializers.Serializer):
    api_key = serializers.CharField(max_length = 128, required = True)
    label = serializers.CharField(max_length = 32,required=False, default = "Default label")
    is_enabled = serializers.BooleanField(required=False)

class TransactionSerializer(serializers.Serializer):
    rfid = RFIDSerializer()
    pos = PoSSerializer()
    amount = serializers.IntegerField(required = True)
    lat = serializers.FloatField(required = False)
    lan = serializers.FloatField(required = False)
    txn_status = serializers.CharField(required = False)
    timestamp = serializers.DateTimeField(required = False)
    txn_id = serializers.CharField(max_length = 128, required = False)

class SpendingRulesSerializer(serializers.Serializer):
    enable_next_txn = serializers.BooleanField(default=False, required=False)
    per_txn_amt_limit = serializers.IntegerField(default=100, required=False)
    total_txn_amt_limit = serializers.IntegerField(default=300, required=False)
    txn_no_limit = serializers.IntegerField(default=15, required=False)

    total_txn_amt = serializers.IntegerField(default=0, required=False)
    txn_no = serializers.IntegerField(default=0, required=False)
    reset_period = serializers.IntegerField(default=24 * 3600)
    start_time = serializers.IntegerField(default=time.time())

    user = EndUserSerializer()

    def create(self, validated_data):
        return SpendingRules(**validated_data)
