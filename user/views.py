from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from dj_rest_auth.views import LoginView
from django.contrib.auth.models import update_last_login

class DeleteUserView(APIView):
    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_200_OK)

# class CustomLoginView(LoginView):
    
#     def post(self, request, *args, **kwargs):
#         self.request = request
#         self.serializer = self.get_serializer(data=self.request.data)
#         self.serializer.is_valid(raise_exception=True)
        
#         print("****************       ", self.request.data['email'])
#         print("****************       ", self.request.data['password'])
#         print("****************       ", self.serializer.data['email'])
#         self.login()
#         update_last_login(None, self.request.data)
#         return self.get_response()

