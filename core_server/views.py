from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core_server.models import EndUser,RFID
from rest_framework.authtoken.models import Token
from core_server.serializer import EndUserSerializer, RFIDSerializer
import time
import hashlib
# Create your views here.

class AddUser(APIView):

    def post(self, request, format = None):
        serializer = EndUserSerializer(data = request.data)

        if serializer.is_valid():
            
            if User.objects.filter(username = serializer.validated_data['username']).count() > 0:
                return Response(data = {"error":"User already exists"},status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create(username = serializer.validated_data['username'])
            user.set_password(serializer.validated_data['password'])
            user.save()
            enduser = EndUser.objects.create(balance = 0,django_user = user, name = serializer.validated_data['name'])       
            enduser.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request, format=None):    
        serializer = EndUserSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print("uname: %s pass: %s"%(username,password))
            user = authenticate(username = username,password = password)
            if Token.objects.filter(user = user).count() > 0:
                token = Token.objects.get(user=user)
            else:
                token = Token.objects.create(user=user)
            return Response(data={"token":token.key}, status=status.HTTP_200_OK)
        
            #except:
            #    return Response({'Error':'Invalid Username or Password'}, status =status.HTTP_401_UNAUTHORIZED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class RFIDView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer  = RFIDSerializer(data = request.data)

        if serializer.is_valid():
            rand_string = request.user.username + str(time.time())
            rfid_value = hashlib.sha1(rand_string.encode('utf-8')).hexdigest()
            label = serializer.validated_data['label']
            is_enabled = False
            enduser = EndUser.objects.get(django_user = request.user)
            rfid = RFID.objects.create(rfid_value = rfid_value, label = label, is_enabled = is_enabled, user = enduser)
            rfid.save()
            return Response(data= RFIDSerializer(rfid).data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
