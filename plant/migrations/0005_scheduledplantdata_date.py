# Generated by Django 3.2 on 2023-09-10 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0004_alter_partner_plant_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledplantdata',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]