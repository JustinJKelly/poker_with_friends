# Generated by Django 3.0.7 on 2020-06-13 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='current_num_players',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='table',
            name='max_players',
            field=models.IntegerField(default=2),
        ),
    ]