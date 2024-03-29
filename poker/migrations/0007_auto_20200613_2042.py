# Generated by Django 3.0.7 on 2020-06-14 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0006_auto_20200613_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='dealer',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='flop_card1',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='flop_card2',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='flop_card3',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1_card1',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1_card2',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1_current_stack',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1_last_bet_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1_last_move',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2_card1',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2_card2',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2_current_stack',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2_last_bet_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2_last_move',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='pot_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table',
            name='river_card',
            field=models.CharField(default='none', max_length=16),
        ),
        migrations.AlterField(
            model_name='table',
            name='turn_card',
            field=models.CharField(default='none', max_length=16),
        ),
    ]
