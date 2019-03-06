from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core_server.models import EndUser
from core_server.serializer import EndUserSerializer, LoginSerializer
import jwt,json
# Create your views here.

class AddUser(APIView):

    def post(self, request, format = None):
        serializer = EndUserSerializer(data = request.data)

        if serializer.is_valid():
            user = User.objects.create(username = serializer.validated_data['username'])
            user.set_password(serializer.validated_data['password'])
            user.save()
            enduser = EndUser.objects.create(balance = 0,django_user = user, name = serializer.validated_data['name'])       
            enduser.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request, format=None):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status="400")
        
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
        try:
            user = authenticate(username = username,password = password)
        except:
            return Response({'Error':'Invalid Username or Password'}, status ='400')

        if user:
            payload = {
                username:user.username
            }
            jwt_token = {'token':jwt.encode(payload,'SECRET')}

            return Response(jwt_token,status=200)

        else:
            return Response(
                json.dumps({'Error': "Invalid credentials"}),
                status=400,
            )

