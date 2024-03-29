# Generated by Django 3.2 on 2023-09-10 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0002_auto_20230810_0127'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledPlantData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('light', models.IntegerField(blank=True, null=True)),
                ('humid', models.IntegerField(blank=True, null=True)),
                ('temp', models.IntegerField(blank=True, null=True)),
                ('soil', models.IntegerField(blank=True, null=True)),
                ('partner_id', models.ForeignKey(db_column='partner_id', on_delete=django.db.models.deletion.CASCADE, related_name='partner', to='plant.partner')),
            ],
        ),
    ]
