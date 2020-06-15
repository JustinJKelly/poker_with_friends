# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<username>\w+)/$', consumers.ChatConsumer),
    #re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/poker/(?P<room_name>\w+)/newUserConnected/(?P<username>\w+)/$', consumers.NewPlayerConsumer),
    #re_path(r'ws/poker/(?P<room_name>\w+)/checkBetCall/(?P<username>/w+)/$', consumers.PokerCheckBetCallConsumer),
    #re_path(r'ws/poker/(?P<room_name>\w+)/start/$', consumers.PokerStartConsumer),
    #re_path(r'ws/poker/(?P<room_name>\w+)/newPlayerEntered/(?P<username>/w+)/$', consumers.NewPlayerEnteredConsumer),
]