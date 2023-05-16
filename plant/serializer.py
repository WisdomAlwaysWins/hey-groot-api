from rest_framework import serializers
from .models import *

class RequestSerializer(serializers.ModelSerializer):
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