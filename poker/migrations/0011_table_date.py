# Generated by Django 3.0.7 on 2020-08-27 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0010_auto_20200721_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]