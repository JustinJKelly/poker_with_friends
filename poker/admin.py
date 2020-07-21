from django.contrib import admin
from .models import  Player
from channels_presence.models import Room
# Register your models here.

#admin.site.register(Table)
admin.site.register(Player)
admin.site.register(Room)