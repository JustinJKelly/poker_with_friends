from django.db import models
from datetime import date
from jsonfield import JSONField

# Create your models here.
class Player(models.Model):
    username = models.CharField(max_length=12,null=False)
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
    players = JSONField()
    