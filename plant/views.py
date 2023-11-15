from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import *
from .serializer import *
from user.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from datetime import datetime
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.tools import BaseTool
from .response_generator import ResponseGenerator
from .chatbot_name import ChatBotName
from .plant_info import PlantInfo as PI
from .plant_for_sensor import PlantSensor
from langchain.agents import AgentType
from pathlib import Path
import environ

import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
from langchain.tools import BaseTool
import pickle
import json
import random


MODEL_PATH = 'static/sentence_transformer_model.pkl'
JSON_PATH = 'static/embedding_data.json'

with open(MODEL_PATH, 'rb') as f:
  model = pickle.load(f)

with open(JSON_PATH, 'r') as f:
    data = json.load(f)
    
# secret key 설정
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')  
# SECRET_KEY = env('SECRET_KEY')
# load_dotenv()

# LangChain 클래스

'''

  이전 대화 코드 
  

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

def get_response(query, user):
  
    partner = Partner.objects.filter(user_id = user).first()
    
    scheduledData = ScheduledPlantData.objects.filter(partner_id = partner).last()
  
    # 고정된 센서 값
    sensor_values = {
        '${l}': scheduledData.light, # 조도 (나옴)
        '${t}': scheduledData.temp, # 온도 (나옴)
        '${h}': scheduledData.humid, # 습도 (나오면 안됨)
        '${m}': scheduledData.soil # 수분 (나오면 안됨)
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
'''

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
        
        if p == None :
          print(request.data['plant_id'], "인덱스 값에서 벗어남")
          return Response({
            "message" : "식물 정보 인덱스 값에서 벗어났습니다."
          }, status = status.HTTP_400_BAD_REQUEST)
          
        print(request.data['plant_id'], p.cntntsSj)
        
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
        bookmark = Bookmark.objects.filter(user_id = request.user.id).order_by('plantinfo__id')
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
        request.POST._mutable = True
        request.data['user_id'] = request.user.id
        request.POST._mutable = False
        partner = Partner.objects.filter(user_id = request.user).last()
        
        print
        
        if partner :
          print("파트너 등록 : 이미 있음")
          return Response({
                "message" : "이미 생성 완료"
          }, status = status.HTTP_400_BAD_REQUEST)
        else :
            print("파트너 등록 : 하고 있음")
            character = Character.objects.get(id = request.data['character_id'])
            serializer = PartnerUpdateSerializer(data = request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self, request):
      
        partner = Partner.objects.get(user_id = request.user).last()  
        
        serializer = PartnerUpdateSerializer(partner, request.data, partial=True)
        
        serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ChatView(APIView):
  
  def post(self, request): # 대화
    partner = Partner.objects.filter(user_id = request.user.id).last()
    
    if partner == None :
      return Response({
        "message" : "현재 등록된 식물이 없어 대화를 진행할 수 없습니다. 식물 정보를 등록해주세요."
      }, status=status.HTTP_400_BAD_REQUEST)
      
    plantName = partner.plant_id.cntntsSj
      
    partnerName = partner.name
    
    datas = ScheduledPlantData.objects.filter(partner_id = partner).last()
    
    t = datas.temp
    h = datas.humid
    i = datas.light
    m = datas.soil
    
    data = [t, h, i, m]
    
    ChatBotName_tool = Tool(
      name="chatbot_name",
      func=ChatBotName(partner_name=partnerName, plant_name=plantName).run,
      description =  "It's a tool used for greeting or asking names, with phrases like 'Nice to meet you', 'Hello', 'What's your name?', 'Who are you?', and it only retrieves responses from ChatBotName_tool. Not used when asking where someone lives."
    )
    
    response_tool = Tool(
      name="response_generator",
      func=ResponseGenerator().run,
      description="""It's a tool used for everyday conversation with plants. Examples include responses like 'Are you sleeping?', 'Where you live', 'Where were you born?', 'I'm hungry'. Responses are only retrieved from response_generator."""
    )

    sensor_tool = Tool(
        name='sensor_tool',
        func= PlantSensor(data=data, plant_type=plantName).run,
        description="""The tool used for receiving a random response from among those generated when asked questions about temperature, humidity, moisture, and sunlight by a user."""
    )

    plant_info_tool = Tool(
        name='plant_info_tool',
        func= PI().run,
        description="""It's a good tool to use when asking about plant information. Summarize it in 100 characters"""
    )

    tools = [response_tool ,sensor_tool, plant_info_tool, ChatBotName_tool]

    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )

    # create our agent
    conversational_agent = initialize_agent(
        agent=AgentType.OPENAI_FUNCTIONS,
        tools=tools,
        llm=ChatOpenAI(temperature=0.1, model="gpt-4-1106-preview"),
        verbose=False,
        max_iterations=5,
        early_stopping_method='generate',
        memory=memory
    )

    question = request.data['question']
      
    if question :
        # answer = get_response(question, request.user)
        answer = conversational_agent.run(question)
        
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
    partner = Partner.objects.filter(user_id = request.user.id).last()

    print(partner)
    
    if partner :
      # print(partner)
      datas = ScheduledPlantData.objects.filter(partner_id = partner)
      instance = {
        'partner' : partner,
        'datas' : datas,
      }
      serializer = PartnerScheduledDataSerializer(instance=instance)
      return Response(serializer.data, status=status.HTTP_200_OK)
      
    else : 
      print("없어요")
      return Response({
        "message" : "등록된 파트너 정보가 없습니다."
      }, status=status.HTTP_400_BAD_REQUEST)

  def post(self, request) :

    partner_id = Partner.objects.get(id = request.data['partner_id'])
    light = float(request.data['light'])
    humid = float(request.data['humid'])
    temp = float(request.data['temp'],)
    soil = int(request.data['soil'])
    
    new_data = {
      'partner_id' : request.data['partner_id'],
      'light' : light,
      'humid' :  humid ,
      'temp' : temp,
      'soil' : soil,
    }
    
    lastest_data = ScheduledPlantData.objects.filter(partner_id = partner_id).last()
    
    if lastest_data == None :
      serializer = ScheduledPlantDataDetailSerializer(data=new_data)
      
      if serializer.is_valid() :
        ScheduledData = ScheduledPlantData.objects.create(
            partner_id = Partner.objects.get(id = request.data['partner_id']),
            # date = request.data['date'],
            light = request.data['light'],
            humid = request.data['humid'],
            temp = request.data['temp'],
            soil = soil,
          )
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    else :
      flag = 0
      
      if abs(lastest_data.light - light) > 50 :
        new_data[light] = light
        flag = 1
      if abs(lastest_data.humid - humid) > 10 :
        new_data[humid] = humid
        flag = 1
      if abs(lastest_data.temp - temp) > 3 :
        new_data[temp] = temp
        flag = 1
      if abs(lastest_data.soil - soil) > 5 :
        new_data[soil] = soil
        flag = 1
        
      serializer = ScheduledPlantDataDetailSerializer(data=new_data)
        
      if serializer.is_valid() :
        if flag == 1 :
          ScheduledData = ScheduledPlantData.objects.create(
            partner_id = Partner.objects.get(id = request.data['partner_id']),
            # date = request.data['date'],
            light = request.data['light'],
            humid = request.data['humid'],
            temp = request.data['temp'],
            soil = soil
          )
          return Response(serializer.data, status = status.HTTP_201_CREATED)
        else :
          date_diff = datetime.now() - lastest_data.date
          if (date_diff.seconds / 60) > 30 :
            ScheduledData = ScheduledPlantData.objects.create(
              partner_id = Partner.objects.get(id = request.data['partner_id']),
              # date = request.data['date'],
              light = request.data['light'],
              humid = request.data['humid'],
              temp = request.data['temp'],
              soil = soil
            )
            return Response(serializer.data, status = status.HTTP_201_CREATED)
          return Response({"msg" : "nothing change"}, status = status.HTTP_200_OK)
      else : 
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


