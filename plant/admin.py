from django.contrib import admin
from .models import *
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'name', 'character_id', 'plant_id', 'is_alarm', 'pot_color')
    
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'plant_id')
    
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'content', 'is_confirm')    
    
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'question', 'answer')
    
@admin.register(PlantInfo)
class PlantInfoAdmin(ImportExportMixin, admin.ModelAdmin):
  ordering = ['id']
  list_display = ['id', 'cntntsNo', 'cntntsSj']
  
@admin.register(ScheduledPlantData)
class ScheduledPlantDataAdmin(admin.ModelAdmin) :
  list_display = ('id', 'partner_id', 'light', 'humid', 'temp', 'soil', 'date')