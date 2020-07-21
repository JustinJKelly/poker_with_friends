
# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels_presence.models import Room
from .models import Table
from .poker_hand import checkHands
from .deal_cards import deal_cards
from time import sleep

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
        
        table = Table.objects.get(table_name=self.room_name)
        text_data_json = json.loads(text_data)
        sentby = text_data_json['sentby']
        decision = text_data_json['decision']
        
        if table.player1 == sentby:
            player1_stack = text_data_json['sentby_stack']
            player2_stack = text_data_json['other_stack']
            player1_bet = text_data_json['sentby_bet']
            player2_bet = text_data_json['other_bet']
        else:
            player2_stack = text_data_json['sentby_stack']
            player1_stack = text_data_json['other_stack']
            player2_bet = text_data_json['sentby_bet']
            player1_bet = text_data_json['other_bet']
            
        table.player1_current_stack = player1_stack
        table.player2_current_stack = player2_stack
        table.player1_last_bet_amount = player1_bet
        table.player2_last_bet_amount = player2_bet
            
        turn = text_data_json['new_turn']
        if table.player1 == turn:
            table.player1_turn = True
            table.player2_turn = False
        else:
            table.player2_turn = True
            table.player1_turn = False
            
        pot = text_data_json['pot']
        table.pot_size = pot
        print("pot", pot)
        table.save()
        
        if decision == "bet":
            betamount = text_data_json['betamount']

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'poker_message_bet',
                    'sentby': sentby,
                    'betamount':betamount,
                    'decision':decision,
                    'sentby_stack': text_data_json['sentby_stack'],
                    'other_stack': text_data_json['other_stack'],
                    'sentby_bet': text_data_json['sentby_bet'],
                    'other_bet': text_data_json['other_bet'],
                    'new_turn':turn,
                    'player1': table.player1,
                    'player2': table.player2,
                    'pot':pot,
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
                    'sentby_stack': text_data_json['sentby_stack'],
                    'other_stack': text_data_json['other_stack'],
                    'sentby_bet': text_data_json['sentby_bet'],
                    'other_bet': text_data_json['other_bet'],
                    'new_turn':turn,
                    'player1': table.player1,
                    'player2': table.player2,
                    'pot':pot,
                }
            )
        
        elif decision == "check":
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'poker_message_check',
                    'sentby': sentby,
                    'decision':decision,
                    'sentby_stack': text_data_json['sentby_stack'],
                    'other_stack': text_data_json['other_stack'],
                    'sentby_bet': text_data_json['sentby_bet'],
                    'other_bet': text_data_json['other_bet'],
                    'new_turn':turn,
                    'player1': table.player1,
                    'player2': table.player2,
                    'pot':pot,
                }
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'poker_message_fold',
                    'sentby': sentby,
                    'decision':decision,
                    'sentby_stack': text_data_json['sentby_stack'],
                    'other_stack': text_data_json['other_stack'],
                    'sentby_bet': text_data_json['sentby_bet'],
                    'other_bet': text_data_json['other_bet'],
                    'new_turn':turn,
                    'player1': table.player1,
                    'player2': table.player2,
                    'pot':pot,
                }
            )

    # Receive message from room group
    def poker_message_bet(self, event):
        sentby = event['sentby']
        decision= event['decision']
        betamount = event['betamount']
        player1 = event['player1']
        player2 = event['player2']
        sentby_stack = event['sentby_stack']
        other_stack = event['other_stack']
        sentby_bet = event['sentby_bet']
        other_bet = event['other_bet']
        turn = event['new_turn']
        pot = event['pot']
        
        #print(player1_bet)
        #print(type(player1_bet), type(player1_stack))

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'sentby': sentby,
            'betamount':betamount,
            'decision':decision,
            'sentby_stack': sentby_stack,
            'other_stack': other_stack,
            'sentby_bet': sentby_bet,
            'other_bet': other_bet,
            'turn':turn,
            'pot':pot,
        }))
        
    # Receive message from room group
    def poker_message_call(self, event):
        sentby = event['sentby']
        decision= event['decision']
        callamount = event['callamount']
        player1 = event['player1']
        player2 = event['player2']
        sentby_stack = event['sentby_stack']
        other_stack = event['other_stack']
        sentby_bet = event['sentby_bet']
        other_bet = event['other_bet']
        turn = event['new_turn']
        pot = event['pot']
        
        

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'sentby': sentby,
            'callamount':callamount,
            'decision':decision,
            'sentby_stack': sentby_stack,
            'other_stack': other_stack,
            'sentby_bet': sentby_bet,
            'other_bet': other_bet,
            'turn':turn,
            'pot':pot,
        }))
    
    # Receive message from room group
    def poker_message_check(self, event):
        sentby = event['sentby']
        decision= event['decision']
        player1 = event['player1']
        player2 = event['player2']
        sentby_stack = event['sentby_stack']
        other_stack = event['other_stack']
        sentby_bet = event['sentby_bet']
        other_bet = event['other_bet']
        turn = event['new_turn']
        pot = event['pot']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'sentby': sentby,
            'decision':decision,
            'sentby_stack': sentby_stack,
            'other_stack': other_stack,
            'sentby_bet': sentby_bet,
            'other_bet': other_bet,
            'turn':turn,
            'pot':pot,
        }))
    
     # Receive message from room group
    def poker_message_fold(self, event):
        sentby = event['sentby']
        decision= event['decision']
        player1 = event['player1']
        player2 = event['player2']
        sentby_stack = event['sentby_stack']
        other_stack = event['other_stack']
        sentby_bet = event['sentby_bet']
        other_bet = event['other_bet']
        turn = event['new_turn']
        pot = event['pot']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'sentby': sentby,
            'decision':decision,
            'sentby_stack': sentby_stack,
            'other_stack': other_stack,
            'sentby_bet': sentby_bet,
            'other_bet': other_bet,
            'turn':turn,
            'pot':pot,
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
        #room_name = text_data_json['room_name']
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
        table_name = text_data_json['table_name']
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
                'table_name':table_name
            }
        )

    def send_winner(self, event):
        
        table_name = event['table_name']
        table = Table.objects.get(table_name=table_name)
        sentby = event['sentby']
        
        #skip one so we don't sent the winner multiple times
        #if table.player1 == sentby:

        #checkHands(player1,player1_cards,player2,player2_cards,flop_cards,turn_card_river_card)
        sentby_cards = event['sentby_cards']
        other_cards = event['other_cards']
        other_username = event['other_username']
        flop_cards = event['flop_cards']
        turn_card = event['turn_card']
        river_card = event['river_card']
        flop_cards = [table.flop_card1,table.flop_card2,table.flop_card3]
        turn_card = table.turn_card
        river_card = table.river_card
        
        hand_info = checkHands(sentby,sentby_cards,other_username,other_cards,flop_cards,turn_card,river_card)
        print('hand info:',hand_info)
        current_dealer = event['current_dealer']
        
        winner = hand_info[0]
        print(winner)
        winning_hand = hand_info[1]
        print(winning_hand)
    
            
        self.send(text_data=json.dumps({
            "winner": winner,
            "winning_hand": winning_hand,
            "sentby_hand": hand_info[2][0],
            "sentby_hand_cards": hand_info[1][1:],
            "other_hand": hand_info[3][0],
            "other_hand_cards": hand_info[2][1:],
            "sentby":sentby,
            "skip":"no",
        }))
            
        '''else:
            self.send(text_data=json.dumps({
                "skip":"yes",
            }))'''
            

class DealNewHandConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'dealNewHand_%s' % self.room_name

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
        room_name = text_data_json['table_name']
        current_dealer = text_data_json['dealer']
        print(sentby, ' ', current_dealer)
        
        table = Table.objects.get(table_name=room_name)
        new_dealer = None
        
        if table.player1 == current_dealer:
            table.dealer = table.player2
            new_dealer = table.player2
        else:
            table.dealer = table.player1
            new_dealer = table.player1
        
        cards = deal_cards(2)
        print(cards, " ")
        #print("Look here:",sentby, ' ', table.dealer)
        
        if sentby == table.player1:
            table.player1_card1 = cards[0]
            table.player1_card2 = cards[1]
            table.player2_card1 = cards[2]
            table.player2_card2 = cards[3]
            table.flop_card1 = cards[4]
            table.flop_card2 = cards[5]
            table.flop_card3 = cards[6]
            table.turn_card = cards[7]
            table.river_card = cards[8]
        else:
            table.player2_card1 = cards[0]
            table.player2_card2 = cards[1]
            table.player1_card1 = cards[2]
            table.player1_card2 = cards[3]
            table.flop_card1 = cards[4]
            table.flop_card2 = cards[5]
            table.flop_card3 = cards[6]
            table.turn_card = cards[7]
            table.river_card = cards[8]
        
        table.flop_displayed = False
        table.turn_displayed = False
        table.river_displayed = False
        
        table.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'new_hand',
                'sentby': sentby,
                'room_name': room_name,
                'new_dealer': new_dealer,
            }
        )

    def new_hand(self, event):
        
        table_name = event['room_name']
        table = Table.objects.get(table_name=table_name)
        sentby = event['sentby']
        sleep(10)
        print("Done sleeping")
        
        if sentby == table.player1:
            self.send(text_data=json.dumps({
                "sentby": sentby,
                "sentby_card1": table.player1_card1,
                "sentby_card2": table.player1_card2,
                "other_card1": table.player2_card1,
                "other_card2": table.player2_card2,
                "flop_card1": table.flop_card1,
                "flop_card2": table.flop_card2,
                "flop_card3": table.flop_card3,
                "turn_card": table.turn_card,
                "river_card": table.river_card,
                "skip":"no",
                "dealer":table.dealer,
            }))
        else:
            self.send(text_data=json.dumps({
                "sentby": sentby,
                "sentby_card1": table.player2_card1,
                "sentby_card2": table.player2_card2,
                "other_card1": table.player1_card1,
                "other_card2": table.player1_card2,
                "flop_card1": table.flop_card1,
                "flop_card2": table.flop_card2,
                "flop_card3": table.flop_card3,
                "turn_card": table.turn_card,
                "river_card": table.river_card,
                "skip":"no",
                "dealer":table.dealer,
            }))
            
class AllInConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'allIn_%s' % self.room_name

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
        room_name = text_data_json['table_name']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'all_in',
                'sentby': sentby,
                'room_name': room_name,
            }
        )

    def all_in(self, event):
        sentby = event['sentby']
        table_name = event['room_name']
        table = Table.objects.get(table_name=table_name)
        
        if sentby == table.dealer:
            print("sent1234545677")
            self.send(text_data=json.dumps({
                "sentby": sentby,
            }))
            
            
class ErrorConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'error_%s' % self.room_name

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
        room_name = text_data_json['table_name']
        issue = text_data_json['issue']
        
        if issue == "issue":
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'error',
                    'sentby': sentby,
                    'room_name': room_name,
                }
            )
        else:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'reconnected',
                    'sentby': sentby,
                    'room_name': room_name,
                }
            )

    def error(self, event):
        sentby = event['sentby']
        table_name = event['room_name']
        table = Table.objects.get(table_name=table_name)
        
        if sentby == table.dealer:
            self.send(text_data=json.dumps({
                "sentby": sentby,
                "message_other": "Error in network. Trying to reconnect with opponent. Please Standby.",
                "message_error": "Error in network caused disconnect. Please try to re-enter table with same credentials.",
                "issue": "issue",
            }))
            
    def reconnected(self, event):
        sentby = event['sentby']
        table_name = event['room_name']
        table = Table.objects.get(table_name=table_name)
        table.error = False
        table.player_error = ""
        table.save()
        
        if sentby == table.dealer:
            self.send(text_data=json.dumps({
                "sentby": sentby,
                "issue": "reconnect",
            }))