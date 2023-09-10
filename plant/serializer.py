from rest_framework import serializers
from .models import *

class PlantInfoSerializer(serializers.ModelSerializer) :
  class Meta :
    model = PlantInfo
    fields = '__all__'
    
class RequestSerializer(serializers.ModelSerializer):
    reference_photo = serializers.ImageField(use_url=True)
    
    class Meta :
        model = Request
        fields = ['id', 'user_id', 'content', 'reference_photo', 'is_confirm']

class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta :
        model = Request
        fields = ['content', 'reference_photo', 'is_confirm']

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta :
        model = Bookmark
        fields = ['id', 'user_id', 'plant_id']
        
class CharacterSerializer(serializers.ModelSerializer):
    basic_emo = serializers.ImageField(use_url=True)
    angry_emo = serializers.ImageField(use_url=True)
    sad_emo = serializers.ImageField(use_url=True)
    happy_emo = serializers.ImageField(use_url=True)
    
    class Meta :
        model = Character
        fields = ['id', 'name', 'basic_emo', 'angry_emo', 'sad_emo', 'happy_emo']    
        
class PartnerDetailSerializer(serializers.ModelSerializer):
    character_id = CharacterSerializer()
    plant_id = PlantInfoSerializer()
    class Meta :
        model = Partner
        fields = ['id', 'user_id', 'character_id', 'plant_id', 'name', 'is_alarm', 'pot_color']

class PartnerUpdateSerializer(serializers.ModelSerializer):
    class Meta :
        model = Partner
        fields = ['character_id', 'user_id', 'name', 'plant_id', 'is_alarm', 'pot_color']
        
class ChatSerializer(serializers.ModelSerializer):
    class Meta :
        model = Chat
        fields = ['id', 'question', 'answer', 'date']
  
class ScheduledPlantDataSerializer(serializers.ModelSerializer) :
  class Meta :
    model = ScheduledPlantData
    fields = '__all__'
    
class ScheduledPlantDataDetailSerializer(serializers.ModelSerializer):
  class Meta :
    model = ScheduledPlantData
    fields = ['date', 'light', 'humid', 'temp', 'soil']

class PartnerScheduledDataSerializer(serializers.Serializer) :
  partner = PartnerDetailSerializer()
  datas = ScheduledPlantDataDetailSerializer(many=True)
  # class Meta :
  #   model = ScheduledPlantData
  #   fields = '__all__'