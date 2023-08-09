from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import *
from .serializer import *
from user.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
import pickle

MODEL_PATH = 'static/sentence_transformer_model.pkl'
CSV_PATH = 'static/train_data_with_embeddings.csv'

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

train_data = pd.read_csv(CSV_PATH)
train_data['embedding'] = train_data['embedding'].apply(lambda x: np.array(eval(x)))

#코사인 유사도 계산 함수
def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

def get_response(input_question):
    input_embedding = model.encode(input_question)
    similarities = train_data['embedding'].apply(lambda x: cosine_similarity(input_embedding, x))
    best_match_idx = np.argmax(similarities)
    return train_data.iloc[best_match_idx]['답변']

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
        partner = Partner.objects.filter(user_id = request.user.id)
        
        if partner:
            # print("*************      ", partner)
            serializer = PartnerDetailSerializer(partner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            # print("*************   없어요 없다구요   ", partner)
            return Response({
                "message" : "등록된 대화 상대 정보가 없습니다."
            }, status=status.HTTP_400_BAD_REQUEST)
    
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

class ChatView(APIView):
    def post(self, request):
        question = request.data['question']
        
        if question :
            answer = get_response(question)
            
            chat = Chat.objects.create(
                user_id = request.user,
                question = question,
                answer = answer,
                date = timezone.now()
            )
            return Response({
                "message" : answer
            }, status=status.HTTP_200_OK)
        else :
            return Response({
                
            }, status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request):
        chat = Chat.objects.filter(user_id = request.user.id)
        serializer = ChatSerializer(chat, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlantInfoPagination(PageNumberPagination):
  page_size = 5

class PlantInfoViewSet(viewsets.ModelViewSet):
  queryset = PlantInfo.objects.all()
  serializer_class = PlantInfoSerializer
  pagination_class = PlantInfoPagination
  filter_backends = [filters.SearchFilter]
  search_fields = ['cntntsSj']