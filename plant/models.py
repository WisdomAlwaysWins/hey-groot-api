from django.db import models
from colorfield.fields import ColorField
from user.models import User
from django.utils import timezone

# Create your models here.

# def path(instance, filename):
#     from random import choice
#     import string
#     arr = [choice(string.ascii_letters) for _ in range(8)]
#     pid = ''.join(arr)
#     extension = filename.split('.')[-1]
#     return '%s/%s.%s' % (instance.id, pid, extension)

class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    basic_emo = models.ImageField(upload_to='character/', null=True, blank=True)
    angry_emo = models.ImageField(upload_to='character/', null=True, blank=True)
    sad_emo = models.ImageField(upload_to='character/', null=True, blank=True)
    happy_emo = models.ImageField(upload_to='character/', null=True, blank=True)
    
    def __str__(self) :
        return self.name
    
class Partner(models.Model):
    id = models.AutoField(primary_key=True),
    user_id = models.ForeignKey(User, related_name='master', on_delete=models.CASCADE, db_column='user_id', null=True)
    character_id = models.ForeignKey(Character, related_name='character', on_delete=models.CASCADE, db_column='character_id')
    plant_id = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    is_alarm = models.BooleanField(default=True)
    pot_color = ColorField(default='##f5c542')
    purchase_date  = models.DateTimeField(
        verbose_name="입양 날짜",
        null=True,
        blank=True
    )
    watering_date = models.DateTimeField(
        verbose_name='물 준 날짜',
        null=True,
        blank=True
    )
    
class Bookmark(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, db_column='user_id')
    plant_id = models.CharField(max_length=10, null=False, blank=False)
    
class Request(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, related_name='applicant', on_delete=models.CASCADE, db_column='user_id')
    content = models.TextField('CONTENT')
    reference_photo = models.ImageField(upload_to='request/%Y/%m/%d/', blank=True)
    is_confirm  = models.BooleanField(default=False)
    
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    question = models.TextField("질문")
    answer = models.TextField("응답")
    date = models.DateTimeField(default=timezone.now)