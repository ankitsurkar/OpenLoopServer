from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core_server.models import EndUser,RFID,PoS, Transaction, SpendingRules
from rest_framework.authtoken.models import Token
from core_server.serializer import EndUserSerializer, RFIDSerializer, PoSSerializer, TransactionSerializer, SpendingRulesSerializer
from .SpendingRulesValidator import ValidateSpendingRule
import time
import hashlib

transaction_status = {0: "Successful", 1: "Initiated", 2: "RFID disabled", 3: "PoS disabled", 4: "Insufficient balance", 5: "Spending rule violation"}
SUCCESS = 0
INITIATED = 1
RFID_DISABLED = 2
POS_DISABLED = 3
INSUF_BALANCE = 4
SPEND_RULE_VIO = 5
# Create your views here.

class AddUser(APIView):

    def post(self, request, format = None):
        serializer = EndUserSerializer(data = request.data)

        if serializer.is_valid():
            
            if User.objects.filter(username = serializer.validated_data['django_user']['username']).count() > 0:
                return Response(data = {"error":"User already exists"},status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create(username = serializer.validated_data['django_user']['username'])
            user.set_password(serializer.validated_data['django_user']['password'])
            user.save()
            enduser = EndUser.objects.create(balance = 0,django_user = user, name = serializer.validated_data['name'],phone_no = serializer.validated_data['phone_no'], is_vendor = serializer.validated_data['is_vendor'])       
            enduser.save()
            spending_rule = SpendingRules(user = enduser)
            spending_rule.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

    def post(self, request, format=None):    
        serializer = EndUserSerializer(data = request.data)

        if serializer.is_valid():
            username = serializer.validated_data['django_user']['username']
            password = serializer.validated_data['django_user']['password']
            print("uname: %s pass: %s"%(username,password))
            user = authenticate(username = username,password = password)

            if user is not None:
                
                enduser = EndUser.objects.get(django_user = user)
                if enduser.token is None:
                    token, created = Token.objects.get_or_create(user=user)
                    enduser.token = token.key
                    enduser.save()                
                return Response(data=EndUserSerializer(enduser).data, status=status.HTTP_200_OK)

            else:
                return Response(data=serializer.data, status=status.HTTP_401_UNAUTHORIZED)

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

     #Returns a list of PoSs
    def get(self, request, format =None):
        enduser = EndUser.objects.get(django_user = request.user)
        pos = PoS.objects.filter(vendor = enduser)
        print(pos)
        serializer = PoSSerializer(pos, many = True)
        print(serializer)
        return Response(data= serializer.data, status=status.HTTP_200_OK)
    
    #Disables a PoS
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

class TransactDetails(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format = None):
        enduser = EndUser.objects.get(django_user = request.user)
        if not enduser.is_vendor:
            transactions = Transaction.objects.filter(rfid__user = enduser)
            serializer = TransactionSerializer(transactions, many = True)
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        else:
            transactions = Transaction.objects.filter(pos__vendor = enduser)
            serializer = TransactionSerializer(transactions, many = True)
            return Response(data = serializer.data, status=status.HTTP_200_OK)

    
class TransactAPI(APIView):

    def post(self, request, format = None):
        serializer = TransactionSerializer(data = request.data)

        if serializer.is_valid():
            rfid = RFID.objects.get(rfid_value = serializer.validated_data['rfid']['rfid_value'])
            pos = PoS.objects.get(api_key = serializer.validated_data['pos']['api_key'])
            txn_id = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()
            transaction = Transaction.objects.create(txn_id = txn_id, amount = serializer.validated_data['amount'], lat = serializer.validated_data['lat'], lan = serializer.validated_data['lan'], rfid = rfid, pos = pos)
            transaction.save()

            if not rfid.is_enabled:
                transaction.txn_status = transaction_status[RFID_DISABLED]
                transaction.save()
                return Response(data=TransactionSerializer(transaction).data, status=status.HTTP_428_PRECONDITION_REQUIRED)
            if not pos.is_enabled:
                transaction.txn_status = transaction_status[POS_DISABLED]
                transaction.save()
                return Response(data=TransactionSerializer(transaction).data, status=status.HTTP_428_PRECONDITION_REQUIRED)
            if rfid.user.balance < transaction.amount:
                transaction.txn_status = transaction_status[INSUF_BALANCE]
                transaction.save()
                return Response(data=TransactionSerializer(transaction).data, status=status.HTTP_417_EXPECTATION_FAILED)
            if not ValidateSpendingRule(rfid.user, transaction.amount):
                transaction.txn_status = transaction_status[SPEND_RULE_VIO]
                transaction.save()
                return Response(data=TransactionSerializer(transaction).data, status=status.HTTP_417_EXPECTATION_FAILED)


            enduser = rfid.user
            enduser.balance -= transaction.amount
            pos_user = pos.vendor 
            pos_user.balance += transaction.amount
            enduser.save()
            pos_user.save()
            transaction.txn_status = transaction_status[SUCCESS]
            transaction.save()
            return Response(data=TransactionSerializer(transaction).data, status= status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status= status.HTTP_400_BAD_REQUEST)

                
class SpendingRuleAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = SpendingRulesSerializer(data = request.data)
        
        if serializer.is_valid():
            spendingrule = serializer.create()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        spending_rule = SpendingRules.objects.get(user__django_user = request.user)

        if spending_rule is not None:
            return Response(data=SpendingRulesSerializer(spending_rule).data, status=status.HTTP_200_OK)

        return Response(data=SpendingRulesSerializer().data, status=status.HTTP_400_BAD_REQUEST)



