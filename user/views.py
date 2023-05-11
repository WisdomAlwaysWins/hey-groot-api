from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from django.contrib.auth.models import update_last_login
from .serializers import UserProfileSerializer
import datetime

class DeleteUserView(APIView):
    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_200_OK)

class UpdateLastVisitView(APIView):
    def get(self, request):
        user = User.objects.get(id = request.user.id)
        print("***************    ", user)
        
        now = datetime.datetime.now()
        now_date = now.strftime('%Y-%m-%d %H:%M:%S')
        # print("********************  ", now_date)
        request.data['last_visit'] = now_date
        print("***************    ", request.data['last_visit'])

        serializer = UserProfileSerializer(user, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)