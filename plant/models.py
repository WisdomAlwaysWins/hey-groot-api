from django.db import models
from colorfield.fields import ColorField
from user.models import User

# Create your models here.

def path(instance, filename):
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return '%s/%s.%s' % (instance.id, pid, extension)

class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    basic_emo = models.ImageField(upload_to='appname', null=True)
    angry_emo = models.ImageField(upload_to='appname', null=True)
    sad_emo = models.ImageField(upload_to='appname', null=True)
    happy_emo = models.ImageField(upload_to='appname', null=True)

class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    character_id = models.ForeignKey(Character, related_name='character', on_delete=models.CASCADE, db_column='character_id')
    is_alarm = models.BooleanField(default=True)
    pot_color = ColorField(default='##f5c542')
    
class Bookmark(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, db_column='user_id')
    plant_id = models.CharField(max_length=10, null=False, blank=False)