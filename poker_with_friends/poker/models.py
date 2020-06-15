from django.db import models
from datetime import date
from jsonfield import JSONField

# Create your models here.
class Player(models.Model):
    username = models.CharField(max_length=12,null=False)
    password = models.CharField(max_length=16,null=False)
    chip_count = models.IntegerField(default=0)
    def __str__(self):
        return self.username

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Player'
        verbose_name_plural = 'Players'
        
class Table(models.Model):
    table_id = models.CharField(max_length=16, null=False)
    table_name = models.CharField(max_length=16, default="Table")
    starting_stack = models.IntegerField(null=False)
    big_blind = models.IntegerField(null=False)
    decision_time = models.IntegerField(default=15)
    players = JSONField()
    max_players = models.IntegerField(default=2)
    current_num_players = models.IntegerField(default=0)
    access_code = models.CharField(max_length=16,null=False)
    player1 = models.CharField(max_length=16, default="none")
    player2 = models.CharField(max_length=16, default="none")
    player1_current_stack = models.IntegerField(null=False,default=0)
    player2_current_stack = models.IntegerField(null=False,default=0)
    player1_last_bet_amount = models.IntegerField(null=False,default=0)
    player2_last_bet_amount = models.IntegerField(null=False,default=0)
    player1_turn = models.BooleanField(default=True)
    player2_turn = models.BooleanField(default=False)
    dealer = models.CharField(max_length=16,default="none")
    player1_last_move = models.CharField(max_length=16,default="none")
    player2_last_move = models.CharField(max_length=16,default="none")
    player1_card1 = models.CharField(max_length=16,default="none")
    player1_card2 = models.CharField(max_length=16,default="none")
    player2_card1 = models.CharField(max_length=16,default="none")
    player2_card2 = models.CharField(max_length=16,default="none")
    flop_card1 = models.CharField(max_length=16,default="none")
    flop_card2 = models.CharField(max_length=16,default="none")
    flop_card3 = models.CharField(max_length=16,default="none")
    pot_size = models.IntegerField(default=0)
    turn_card = models.CharField(max_length=16,default="none")
    river_card = models.CharField(max_length=16,default="none")
    
    
    
    
    def __str__(self):
        return self.table_name
    