from rest_framework import serializers
from .models import *

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
    
    class Meta :
        model = Partner
        fields = ['id', 'character_id', 'name', 'purchase_date', 'watering_date', 'is_alarm', 'pot_color']

class PartnerUpdateSerializer(serializers.ModelSerializer):
    class Meta :
        model = Partner
        fields = ['character_id', 'name', 'is_alarm', 'pot_color']
        
        
# class UserProfileSerializer(serializers.ModelSerializer):
#     last_visit = serializers.DateTimeField(format= '%Y-%m-%d %H:%M:%S')
#     class Meta:
#         model = User
#         fields = ['nickname', 'last_visit']