# Generated by Django 3.2 on 2023-05-17 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
