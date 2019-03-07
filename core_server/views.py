from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core_server.models import EndUser,RFID,PoS
from rest_framework.authtoken.models import Token
from core_server.serializer import EndUserSerializer, RFIDSerializer, PoSSerializer
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
            enduser = EndUser.objects.create(balance = 0,django_user = user, name = serializer.validated_data['name'],phone_no = serializer.validated_data['phone_no'])       
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
class PosView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = PoSSerializer(data = request.data)
    
        if serializer.is_valid():
            label = serializer.validated_data['label']
            vendor = EndUser.objects.get(django_user=request.user)
            rand_string = request.user.username + str(time.time())
            api_key = hashlib.sha1(rand_string.encode('utf-8')).hexdigest()
            pos = PoS.objects.create(label = label,api_key=api_key,vendor=vendor)
            pos.save()
            return Response(data = PoSSerializer(pos).data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

     #Returns a list of RFIDs
    def get(self, request, format =None):
        enduser = EndUser.objects.get(django_user = request.user)
        pos = PoS.objects.filter(vendor = enduser)
        print(pos)
        serializer = PoSSerializer(pos, many = True)
        print(serializer)
        return Response(data= serializer.data, status=status.HTTP_200_OK)
    
    #Disables a RFID
    def delete(self, request, format=None):
        serializer = PoSSerializer(data = request.data)

        if serializer.is_valid():
            pos = PoS.objects.filter(api_key = serializer.validated_data['api_key'])
            if pos.count() == 1:
                pos = pos[0]
                pos.is_enabled = False
                pos.save()
                serializer = PoSSerializer(pos)
                return Response(data=serializer.data, status=status.HTTP_200_OK)

            return Response(data={"error":"Invalid PoS value"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RFIDView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    #Creates a new RFID and returns it
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
    
    #Returns a list of RFIDs
    def get(self, request, format =None):
        enduser = EndUser.objects.get(django_user = request.user)
        rfids = RFID.objects.filter(user = enduser)
        print(rfids)
        serializer = RFIDSerializer(rfids, many = True)
        print(serializer)
        return Response(data= serializer.data, status=status.HTTP_200_OK)
    
    #Disables a RFID
    def delete(self, request, format=None):
        serializer = RFIDSerializer(data = request.data)

        if serializer.is_valid():
            rfid = RFID.objects.filter(rfid_value = serializer.validated_data['rfid_value'])
            if rfid.count() == 1:
                rfid = rfid[0]
                rfid.is_enabled = False
                rfid.disability_reason = serializer.validated_data['disability_reason']
                rfid.save()
                serializer = RFIDSerializer(rfid)
                return Response(data=serializer.data, status=status.HTTP_200_OK)

            return Response(data={"error":"Invalid RFID value"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


