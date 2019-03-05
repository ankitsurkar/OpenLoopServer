from rest_framework import serializers
from core_server.models import *

class EndUserSerializer(serializers.Serializer):
    name = serializers.CharField( max_length = 32, required = True)
    password = serializers.CharField(max_length = 32, required = True)
    username = serializers.CharField(max_length = 32, required = True) 


