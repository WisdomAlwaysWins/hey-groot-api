from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import *
from .serializer import *
from user.models import User

# Create your views here.

class RequestListView(APIView):
    # 사용자 요청 모아보기 
    def get(self, request):
        requests = Request.objects.filter(user_id = request.user)
        serializer = RequestSerializer(requests, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    # 요청 추가하기
    def post(self, request):
        serializer = RequestCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            data = Request.objects.create(
                user_id = request.user,
                content = request.data['content'],
                reference_photo = request.data['photo']
            )
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class BookmarkView(APIView):
    # 북마크 등록/해제
    def post(self, request):
        bookmark = Bookmark.objects.filter(plant_id = request.data['plant_id'], user_id = request.user)
        
        if bookmark :
            bookmark[0].delete()
            message = '북마크 해제'
        else :
            Bookmark.objects.create(
                user_id = request.user,
                plant_id = request.data['plant_id'],
            )
            message = '북마크 등록'
        return Response({
            "message" : message
        }, status = status.HTTP_200_OK)

class BookmarkListView(APIView):
    # 북마크 리스트
    def get(self, request):
        bookmark = Bookmark.objects.filter(user_id = request.user.id)
        serializer = BookmarkSerializer(bookmark, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CharacterViewSet(viewsets.ModelViewSet):
    # 캐릭터 CRUD
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    
class PartnerView(APIView):
    def get(self, request):
        partner = Partner.objects.get(user_id = request.user.id)
        print("*************      ", partner)
        serializer = PartnerDetailSerializer(partner)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data._mutable = True
        request.data['user_id'] = request.user.id
        request.data._mutable = False
        partner = Partner.objects.filter(user_id = request.user)
        print(partner)
        
        if partner.exists() :
            return Response({
                "message" : "이미 생성 완료"
            }, status = status.HTTP_400_BAD_REQUEST)
        else :
            character = Character.objects.get(id = request.data['character_id'])
            serializer = PartnerUpdateSerializer(data = request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self, request):
        partner = Partner.objects.get(user_id = request.user.id)
        serializer = PartnerUpdateSerializer(partner, request.data, partial=True)
        serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    