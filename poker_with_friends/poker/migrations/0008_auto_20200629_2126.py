# Generated by Django 3.0.7 on 2020-06-30 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0007_auto_20200613_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='password',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='access_code',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='dealer',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='flop_card1',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='flop_card2',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='flop_card3',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1_card1',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1_card2',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='player1_last_move',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2_card1',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2_card2',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2_last_move',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='river_card',
            field=models.CharField(default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='table_id',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='table_name',
            field=models.CharField(default='Table', max_length=25),
        ),
        migrations.AlterField(
            model_name='table',
            name='turn_card',
            field=models.CharField(default='none', max_length=25),
        ),
    ]
