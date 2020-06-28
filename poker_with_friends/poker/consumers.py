# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels_presence.models import Room
from .models import Table

#NEEDED DIFFERENT GROUP NAMES
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
        self.room_group_name = 'newplayer_%s' % self.room_name
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
        users = Room.objects.get(channel_name="poker_game").get_users()
        print("users:",users)
        if (len(users) == 2):
            self.send(text_data=json.dumps({
                'username': username,
                'game_on':'yes'
            }))
        else:
            # Send message to room group
            self.send(text_data=json.dumps({
                'username': username,
                'game_on':'no'
            }))
            

class PlayerDecisionConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'decision_%s' % self.room_name
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
        sentby = text_data_json['sentby']
        decision = text_data_json['decision']
        
        if decision == "bet":
            betamount = text_data_json['betamount']
            #print('betamount:',betamount)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'poker_message_bet',
                    'sentby': sentby,
                    'betamount':betamount,
                    'decision':decision,
                }
            )
        
        elif decision == "call":
            callamount = text_data_json['callamount']
            print('callamount:',callamount)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'poker_message_call',
                    'sentby': sentby,
                    'callamount':callamount,
                    'decision':decision,
                }
            )
        
        else:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'poker_message_check',
                    'sentby': sentby,
                    'decision':decision,
                }
            )

    # Receive message from room group
    def poker_message_bet(self, event):
        sentby = event['sentby']
        decision= event['decision']
        betamount = event['betamount']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'sentby': sentby,
            'betamount':betamount,
            'decision':decision,
        }))
        
    # Receive message from room group
    def poker_message_call(self, event):
        sentby = event['sentby']
        decision= event['decision']
        callamount = event['callamount']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'sentby': sentby,
            'callamount':callamount,
            'decision':decision,
        }))
    
    # Receive message from room group
    def poker_message_check(self, event):
        sentby = event['sentby']
        decision= event['decision']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'sentby': sentby,
            'decision':decision,
        }))
        
class PlayerFoldedConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'playerFolded_%s' % self.room_name

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


    '''
    handWinnerSocket.send(JSON.stringify({
        'sentby': "{{username}}",
        'sentby_cards': my_cards,
        'opp_cards': opp_cards,
        'flop_cards': flop,
        'turn_card': turn_card,
        'river_card': river_card,
        'opp_username': "{{opp_username}}",
    }));
    '''
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sentby = text_data_json['sentby']
        sentby_cards = text_data_json['sentby_cards']
        other_cards = text_data_json['opp_cards']
        other_username = text_data_json['opp_username']
        flop_cards = text_data_json['flop_cards']
        turn_card = text_data_json['turn_card']
        river_card = text_data_json['river_card']
        current_dealer = text_data_json['current_dealer']
        print(sentby, ' ', sentby_cards, ' ', other_cards, ' ', other_username, ' ', flop_cards, ' ', turn_card, ' ', river_card, ' ', current_dealer)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_winner',
                'sentby': sentby,
                'sentby_cards': sentby_cards,
                'other_cards': other_cards,
                'other_username': other_username,
                'flop_cards': flop_cards,
                'turn_card': turn_card,
                'river_card': river_card,
                'current_dealer': current_dealer,
            }
        )

    def send_winner(self, event):
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
        }))
    
        
class CheckHandWinnerConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'checkHand_%s' % self.room_name

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


    '''
    handWinnerSocket.send(JSON.stringify({
        'sentby': "{{username}}",
        'sentby_cards': my_cards,
        'opp_cards': opp_cards,
        'flop_cards': flop,
        'turn_card': turn_card,
        'river_card': river_card,
        'opp_username': "{{opp_username}}",
    }));
    '''
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sentby = text_data_json['sentby']
        sentby_cards = text_data_json['sentby_cards']
        other_cards = text_data_json['opp_cards']
        other_username = text_data_json['opp_username']
        flop_cards = text_data_json['flop_cards']
        turn_card = text_data_json['turn_card']
        river_card = text_data_json['river_card']
        current_dealer = text_data_json['current_dealer']
        print(sentby, ' ', sentby_cards, ' ', other_cards, ' ', other_username, ' ', flop_cards, ' ', turn_card, ' ', river_card, ' ', current_dealer)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_winner',
                'sentby': sentby,
                'sentby_cards': sentby_cards,
                'other_cards': other_cards,
                'other_username': other_username,
                'flop_cards': flop_cards,
                'turn_card': turn_card,
                'river_card': river_card,
                'current_dealer': current_dealer,
            }
        )

    def send_winner(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
        }))