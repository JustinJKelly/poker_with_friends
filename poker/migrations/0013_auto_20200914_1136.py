# Generated by Django 3.0.7 on 2020-09-14 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0012_savedtable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]