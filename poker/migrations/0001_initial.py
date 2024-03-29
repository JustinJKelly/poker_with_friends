# Generated by Django 3.0.7 on 2020-06-13 00:18

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=16)),
                ('chip_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Player',
                'verbose_name_plural': 'Players',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_id', models.CharField(max_length=16)),
                ('table_name', models.CharField(default='Table', max_length=16)),
                ('starting_stack', models.IntegerField()),
                ('big_blind', models.IntegerField()),
                ('decision_time', models.IntegerField(default=15)),
                ('players', jsonfield.fields.JSONField()),
            ],
        ),
    ]
