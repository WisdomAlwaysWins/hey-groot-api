from rest_framework import serializers
from .models import *

class RequestSerializer(serializers.ModelSerializer):
    class Meta :
        model = Request
        fields = ['id', 'content', 'reference_photo', 'is_confirm']
    