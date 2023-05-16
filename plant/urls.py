from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'plant'

urlpatterns = [
    path('request/', RequestListView.as_view()),
    path('mark/', BookmarkView.as_view()),
    path('mark/list/', BookmarkListView.as_view()),
]
