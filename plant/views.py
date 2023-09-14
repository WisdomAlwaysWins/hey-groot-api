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
import json
import random

MODEL_PATH = 'static/sentence_transformer_model.pkl'
JSON_PATH = 'static/embedding_data.json'

with open(MODEL_PATH, 'rb') as f:
     model = pickle.load(f)

# JSON 데이터 로딩
with open(JSON_PATH, 'r') as f:
    data = json.load(f)

def get_most_similar_question(query):
    # 사용자로부터 입력 받은 질문을 임베딩
    query_embedding = model.encode(query)
    similarities = []

    # 질문에 대해 임베딩을 생성하고 쿼리와의 유사도를 계산
    for question in data.keys():
        question_embedding = model.encode(question)
        # 코사인 유사도 계산식
        similarity = np.dot(query_embedding, question_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(question_embedding))
        similarities.append(similarity)

    # 가장 유사한 질문의 인덱스를 찾음
    most_similar_idx = np.argmax(similarities)
    return list(data.keys())[most_similar_idx]

def get_response(query):
    # 고정된 센서 값
    sensor_values = {
        '${l}': 40000, # 조도 (나옴)
        '${t}': 25, # 온도 (나옴)
        '${h}': 40, # 습도 (나오면 안됨)
        '${m}': 60 # 수분 (나오면 안됨)
    }

    # 센서 값에 따른 임계값
    thresholds = {
        '${l}': 45000,
        '${t}': 30,
        '${h}': 30,
        '${m}': 50
    }

    # 가장 유사한 질문을 가져옴
    most_similar_question = get_most_similar_question(query)
    responses = data[most_similar_question]

    # 해당 질문에 대한 응답 중 하나를 무작위로 선택
    response = random.choice(responses)
    response_text = list(response.values())[0]

    # 센서 값의 임계값을 기준으로 응답을 수정하거나 다시 선택
    for literal, threshold in thresholds.items():
        if literal in response_text:
            # 센서 값으로 템플릿 리터럴 대체
            response_text = response_text.replace(literal, str(sensor_values[literal]))

            if sensor_values[literal] > threshold:
                # 다른 응답을 선택
                responses_without_literal = [resp for resp in responses if literal not in list(resp.values())[0]]
                chosen_response = random.choice(responses_without_literal)
                response_text = list(chosen_response.values())[0]
                # 이전에 대체된 템플릿 리터럴 대체를 다시 반복
                for lit, value in sensor_values.items():
                    if lit in response_text:
                        response_text = response_text.replace(lit, str(value))

    return response_text


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
        
        p = PlantInfo.objects.get(id = request.data['plant_id'])
        
        bookmark = Bookmark.objects.filter(user_id = request.user.id, plantinfo = p)
        
        if bookmark : 
          bookmark[0].delete()
          message = '북마크 해제'
        else :
          Bookmark.objects.create(
            user = request.user,
            plantinfo = p,
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
          serializer = PartnerDetailSerializer(partner, many=True)
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
      
        partner = Partner.objects.get(user_id = request.user, id = request.data['partner_id'])  
        print(partner)
        
        serializer = PartnerUpdateSerializer(partner, request.data, partial=True)
        
        serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
          {'mesg' : 'hi'},
          status = status.HTTP_200_OK
        )
        


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
  
class ScheduledPlantDataView(APIView):
  def get(self, request):
    partner = Partner.objects.filter(user_id = request.user.id)

    if partner :
      partner = partner[0]
      # print(partner)
      datas = ScheduledPlantData.objects.filter(partner_id = partner)
      instance = {
        'partner' : partner,
        'datas' : datas,
      }
      serializer = PartnerScheduledDataSerializer(instance=instance)
      return Response(serializer.data, status=status.HTTP_200_OK)
      
    else : 
      # print("*************   없어요 없다구요   ", partner)
      return Response({
        "message" : "등록된 파트너 정보가 없습니다."
      }, status=status.HTTP_400_BAD_REQUEST)

  # def post(self, request):
    
