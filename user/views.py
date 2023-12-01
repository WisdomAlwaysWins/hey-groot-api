from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from django.contrib.auth.models import update_last_login
from .serializers import *
import datetime

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterUserView(APIView):
  def post(self, request):
    serializer = CustomUserDetailsSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      token = TokenObtainPairSerializer.get_token(user)
      refresh_token = str(token)
      access_token = str(token.access_token)
      res = Response({
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "user" : serializer.data,
      }, status = status.HTTP_201_CREATED)
      return res
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView) :
  def post(self, request):
    user = authenticate(email = request.data['email'], password = request.data['password'])
    
    if user is not None :
      serializer = CustomUserDetailsSerializer(user)
      token = TokenObtainPairSerializer.get_token(user)
      refresh_token = str(token)
      access_token = str(token.access_token)
      res = Response({
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "user" : serializer.data,
      }, status = status.HTTP_200_OK)
      return res
    else :
      return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class DeleteUserView(APIView):
    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_200_OK)

class UpdateUserInfoView(APIView):
    def get(self, request):
        user = User.objects.get(id = request.user.id)
        print("** ", user)
        
        now = datetime.datetime.now()
        now_date = now.strftime('%Y-%m-%d %H:%M:%S')
        # print("********************  ", now_date)
        request.data['last_visit'] = now_date
        print("** ", request.data['last_visit'])

        serializer = UserProfileSerializer(user, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        user = User.objects.get(id = request.user.id)
        serializer = UserProfileSerializer(user, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)