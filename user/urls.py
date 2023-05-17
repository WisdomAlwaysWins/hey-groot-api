from django.urls import path, include
from .views import *

app_name = 'user'

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path("auth/delete/", DeleteUserView.as_view(), name="delete"),
    path('update/', UpdateUserInfoView.as_view(), name='update-user-info')
    # path("login/", CustomLoginView.as_view(), name="login")
    
]