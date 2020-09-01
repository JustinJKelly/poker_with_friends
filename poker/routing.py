# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<username>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/poker/(?P<room_name>\w+)/newUserConnected/(?P<username>\w+)/$', consumers.NewPlayerConsumer),
    re_path(r'ws/poker/(?P<room_name>\w+)/playerDecision/(?P<username>\w+)/$', consumers.PlayerDecisionConsumer),
    re_path(r'ws/poker/(?P<room_name>\w+)/getHandWinner/$', consumers.CheckHandWinnerConsumer),
    re_path(r'ws/poker/(?P<room_name>\w+)/fold/$', consumers.PlayerFoldedConsumer),
    re_path(r'ws/poker/(?P<room_name>\w+)/dealNewHand/$', consumers.DealNewHandConsumer),
    re_path(r'ws/poker/(?P<room_name>\w+)/deleteGame/$', consumers.DeleteGameConsumer),
    re_path(r'ws/poker/(?P<room_name>\w+)/allIn/$', consumers.AllInConsumer),
    re_path(r'ws/poker/(?P<room_name>\w+)/errorSocket/$', consumers.ErrorConsumer),
]