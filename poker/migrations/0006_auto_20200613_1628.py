# Generated by Django 3.0.7 on 2020-06-13 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0005_auto_20200613_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='flop_card1',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='flop_card2',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='flop_card3',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='player1_card1',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='player1_card2',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='player1_last_move',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='player2_card1',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='player2_card2',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='player2_last_move',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='pot_size',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='river_card',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='turn_card',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
    ]