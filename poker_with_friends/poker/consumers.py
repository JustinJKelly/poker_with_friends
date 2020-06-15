# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels_presence.models import Room
from .models import Table

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username':username
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username':username
        }))
        
class NewPlayerConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'poker_%s' % self.room_name
        self.username_connected = self.scope['url_route']['kwargs']['username']
        print(self.username_connected)
        Room.objects.add("poker_game", self.channel_name, self.scope["user"])
        print(self.scope["user"])
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        
        '''num_users = Room.objects.get(channel_name="poker_game").get_users()
        print(num_users)
        
        if (len(num_users) == 2):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'game_message',
                    'username': self.username_connected,
                    'game_on':'yes'
                }
            )
        else:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'poker_message',
                    'username': self.username_connected,
                    'game_on':'no'
                }
            )'''
            

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json['username']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'game_on',
                'username': username,
            }
        )

    def game_on(self, event):
        username = event['username']
        
        num_users = Room.objects.get(channel_name="poker_game").get_users()
        print(num_users)
        
        if (len(num_users) == 2):
            self.send(text_data=json.dumps({
                'username': self.username_connected,
                'game_on':'yes'
            }))
        else:
            # Send message to room group
            self.send(text_data=json.dumps({
                'username': self.username_connected,
                'game_on':'no'
            }))
        
    # Receive message from room group
    def poker_message(self, event):
        username = event['username']
        game_on = event['game_on']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'username': username,
            'game_on': game_on
        }))
        

class PokerCheckBetCallConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'poker_%s' % self.room_name
        #Room.objects.add("some_room", self.channel_name, self.scope["user"])

        print(self.room_group_name + " " + self.channel_name)
        print(Room)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json['username']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'poker_message',
            }
        )

    # Receive message from room group
    def poker_message(self, event):

        # Send message to WebSocket
        self.send(text_data=json.dumps({

        }))
        
class PokerStartConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'poker_%s' % self.room_name
        #Room.objects.add("some_room", self.channel_name, self.scope["user"])

        print(self.room_group_name + " " + self.channel_name)
        print(Room)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        #player1 = text_data_json['player1']
        #player2 = text_data_json['player2']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'start_game',
            }
        )

    # Receive message from room group
    def start_game(self, event):

        # Send message to WebSocket
        self.send(text_data=json.dumps({

        }))
        
class NewPlayerEnteredConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'poker_%s' % self.room_name
        #Room.objects.add("some_room", self.channel_name, self.scope["user"])

        print(self.room_group_name + " " + self.channel_name)
        print(Room)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'update_Opp',
            }
        )

    # Receive message from room group
    def update_Opp(self, event):

        # Send message to WebSocket
        self.send(text_data=json.dumps({
        }))    
        