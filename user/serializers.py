from django.conf import settings
from .models import User
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.get("password")
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('pk', 'email', 'nickname','last_login')
        read_only_fields = ('email', 'last_login' )
        

class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user('', email, password)
        user1 = authenticate(attrs, email=email, password=password)

        print("** 로그인한 사용자 이메일 :", email)
        
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user)

        update_last_login(None, user1)
        
        attrs['user'] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    last_visit = serializers.DateTimeField(format= '%Y-%m-%d %H:%M:%S')
    class Meta:
        model = User
        fields = ['nickname', 'last_visit']
