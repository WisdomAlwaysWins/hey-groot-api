from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'plant'

character_list = CharacterViewSet.as_view({
    'get' : 'list',
    'post' : 'create'
})

character_detail = CharacterViewSet.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'delete' : 'destroy'
})

plantInfo_list = PlantInfoViewSet.as_view({
  'get' : 'list',
  'post' : 'create'
})

plantInfo_detail = PlantInfoViewSet.as_view({
  'get' : 'retrieve',
  'put' : 'update',
  'delete' : 'destroy',
})

urlpatterns = [
    path('request/', RequestListView.as_view()),
    path('mark/', BookmarkView.as_view()),
    path('mark/list/', BookmarkListView.as_view()),
    path('characters/', character_list),
    path('characters/<int:pk>/', character_detail),
    path('partner/', PartnerView.as_view()),
    path('chat/', ChatView.as_view()),
    path('plants/', plantInfo_list),
    path('plants/detail/<int:pk>/', plantInfo_detail),
]
