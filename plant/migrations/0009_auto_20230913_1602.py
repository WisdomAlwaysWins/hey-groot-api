# Generated by Django 3.2 on 2023-09-13 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0008_alter_bookmark_plant_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='plant_id',
            new_name='plantinfo',
        ),
        migrations.RenameField(
            model_name='bookmark',
            old_name='user_id',
            new_name='user',
        ),
    ]