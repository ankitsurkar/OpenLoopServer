from rest_framework import serializers
from core_server.models import *

class EndUserSerializer(serializers.Serializer):
    name = serializers.CharField( max_length = 32, required = True)
    password = serializers.CharField(max_length = 32, required = True)
    username = serializers.CharField(max_length = 32, required = True) 


class RFIDSerializer(serializers.Serializer):
    rfid_value = serializers.CharField(max_length = 128,required = True)
    label = serializers.CharField(max_length = 32, required = False)
    is_enabled = serializers.BooleanField(required = False)
    disability_reason = serializers.CharField(max_length = 32, required = False)
