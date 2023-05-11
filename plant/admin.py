from django.contrib import admin
from .models import *

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'character_id', 'is_alarm', 'pot_color')
    
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'plant_id')