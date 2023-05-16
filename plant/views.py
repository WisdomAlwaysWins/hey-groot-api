from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *

# Create your views here.

class RequestListView(APIView):
    # 사용자 요청 모아보기 
    def get(self, request):
        requests = Request.objects.filter(user = request.user)
        serializer = RequestSerializer(requests, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    # 요청 추가하기
    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        
        if serializer.is_valid():
            data = Request.objects.create(
                user_id = request.user,
                content = request.data['context'],
                reference_photo = request.data['photo']
            )
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        