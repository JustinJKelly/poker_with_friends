from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MakeTableForm, JoinTableForm, SubmitRequestForm
from django.contrib import messages
from .models import Table
from .deal_cards import deal_cards
from django.urls import reverse
import string
import random
from django.utils.html import escape
from django.core.mail import EmailMessage, BadHeaderError, send_mail
from django.conf import settings
from django.utils import timezone
import pytz
from datetime import datetime

# Create your views here.
def make_table(request):
    if request.method == 'POST':
        #print(request.POST)
        form = MakeTableForm(request.POST)
        tables = Table.objects.all()
        
        if len(tables) >= 5 and request.POST['table_name'].replace(" ", "") != "WeDemBois":
            return HttpResponse("No tables available. Please check back later when rooms are available")
        elif form.is_valid():
            #print(request.POST)
            if int(request.POST['big_blind']) % 2 != 0:
                messages.add_message(request, messages.ERROR, 'Error in processing form data. Big blind must be an even number!')
                form = MakeTableForm()
                return render(request,"poker/make_table.html",{'form':form})
            elif len(request.POST['table_name']) == 0 or len(request.POST['access_code']) == 0:
                messages.add_message(request, messages.ERROR, 'Error in processing form data. Table name and access code can not be empty!')
                form = MakeTableForm()
                return render(request,"poker/make_table.html",{'form':form})
            elif " " in request.POST['table_name'] or " " in request.POST['access_code']:
                messages.add_message(request, messages.ERROR, 'Error in processing form data. Table name and access code can not have spaces!')
                form = MakeTableForm()
                return render(request,"poker/make_table.html",{'form':form})
            else:
                new_table_name = request.POST['table_name'].replace(" ", "")
                tables = Table.objects.filter(table_name=new_table_name)

                if len(tables) > 0:
                    #print(len(tables))
                    new_table_name = new_table_name + "_" + create_table_string()
                new_table = Table(date=datetime.now(tz=timezone.utc), table_id=create_table_id(), table_name=new_table_name, starting_stack=request.POST['starting_stack'].replace(" ", ""), big_blind=request.POST['big_blind'].replace(" ", ""), access_code=request.POST['access_code'].replace(" ", ""))
                new_table.save()
                messages.add_message(request, messages.SUCCESS, 'Table created! Table name is ' + new_table_name)
                return redirect("/poker/join_table")
        else:
            messages.add_message(request, messages.ERROR, 'Error in processing form data.')
            form = MakeTableForm()
            return render(request,"poker/make_table.html",{'form':form})
        return HttpResponse("Thanks")
    
    form = MakeTableForm()
    return render(request, "poker/make_table.html", {"form": form})

def create_table_id():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(16))

def create_table_string():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(4))

# Create your views here.
def join_table(request):
    if request.method == 'POST':
        form = JoinTableForm(request.POST)
        if form.is_valid():
            #print(request.POST['chosen_table'])
            #print(request.POST['access_code'])
            #print(request.POST['username'])
            username = request.POST['username'].replace(" ", "")
            table = Table.objects.get(table_id=request.POST['chosen_table'])
            if request.POST['access_code'] == table.access_code:
                if table.player1 == "none": 
                    table.player1 = username
                    table.save()
                elif table.player2 == "none": 
                    if table.player1 == username:
                        username = username + "2"
                        table.player2 = username
                    else:
                        table.player2 = username 
                    table.save()
                elif table.error:
                    if table.player1 == username or table.player2 == username:
                        redirect = HttpResponseRedirect("/poker/table/"+table.table_name)
                        request.session['username'] = username
                        request.session['table_id'] = request.POST['chosen_table']
                        return redirect
                    else:
                        return HttpResponse("Table full")
                        
                else:
                    return HttpResponse("Table full")
                redirect = HttpResponseRedirect("/poker/table/"+table.table_name)
                request.session['username'] = username
                request.session['table_id'] = request.POST['chosen_table']
                return redirect
            else:
                messages.add_message(request, messages.ERROR, 'Error in processing form data: Wrong access code!')
                form = JoinTableForm()
                return render(request,"poker/join_table.html",{'form':form})
        else:
            messages.add_message(request, messages.ERROR, 'Error in processing form data')
            form = JoinTableForm()
            return render(request,"poker/join_table.html",{'form':form})

    form = JoinTableForm()
    return render(request, "poker/join_table.html", {"form": form})

'''
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
'''
#start game
def room(request, room_name):
    #table = Table.objects.get(table_id=request.session.get('table_id'))
    return redirect("/poker/table/"+request.session.get('table_id')+"/"+room_name)

def room_protected(request,room_name,table_id,):
    table = Table.objects.get(table_id=table_id)
    #print("look here",table.table_name)
    context = {}
    if 'username' in request.session:
        username = request.session.get('username')
        context['username'] = username
    else:
        context['username'] = "username"
    
    if table.player2 == "none":
        cards = deal_cards(2)
        table.dealer = username
    
        #print(cards, " ")
        
        table.player1_card1 = cards[0]
        table.player1_card2 = cards[1]
        table.player2_card1 = cards[2]
        table.player2_card2 = cards[3]
        table.flop_card1 = cards[4]
        table.flop_card2 = cards[5]
        table.flop_card3 = cards[6]
        table.turn_card = cards[7]
        table.river_card = cards[8]
        table.pot_size = 0
        table.player2_last_bet_amount = 0
        table.player1_last_bet_amount = 0
        table.player2_current_stack = table.starting_stack
        table.player1_current_stack = table.starting_stack
        table.save()
    
    
    context['room_name'] = room_name
    if table.player1 != "none" and table.player2 != "none":
        context["game_on"] = "game_on"
        print("GAME ON")
    else:
        context["game_on"] = "no"
        
    context['starting_stack'] = table.starting_stack
    context['big_blind'] = table.big_blind
    context['small_blind'] = float(table.big_blind/2)
    context['decision_time'] = table.decision_time
    
    if table.player1 == username:
        context['card1'] = table.player1_card1
        context['card2'] = table.player1_card2
        context['opp_card1'] = table.player2_card1
        context['opp_card2'] = table.player2_card2
        context['my_username'] = table.player1
        context['opp_username'] = table.player2
        context['my_last_bet_amount'] = table.player1_last_bet_amount
        context['opp_last_bet_amount'] = table.player2_last_bet_amount
        context['my_curr_stack'] = table.player1_current_stack
        context['opp_curr_stack'] = table.player2_current_stack
        context['my_last_bet_amount'] = table.player1_last_bet_amount
        context['opp_last_bet_amount'] = table.player2_last_bet_amount
        context['my_turn'] = table.player1_turn
        context['opp_turn'] = table.player2_turn
        context['flop_card1'] = table.flop_card1
        context['flop_card2'] = table.flop_card2
        context['flop_card3'] = table.flop_card3
        context['pot_size'] = table.pot_size
        context['turn_card'] = table.turn_card
        context['river_card'] = table.river_card
    else:
        context['card1'] = table.player2_card1
        context['card2'] = table.player2_card2
        context['opp_card1'] = table.player1_card1
        context['opp_card2'] = table.player1_card2
        context['my_username'] = table.player2
        context['opp_username'] = table.player1
        context['my_last_bet_amount'] = table.player2_last_bet_amount
        context['opp_last_bet_amount'] = table.player1_last_bet_amount
        context['my_curr_stack'] = table.player2_current_stack
        context['opp_curr_stack'] = table.player1_current_stack
        context['my_last_bet_amount'] = table.player2_last_bet_amount
        context['opp_last_bet_amount'] = table.player1_last_bet_amount
        context['my_turn'] = table.player2_turn
        context['opp_turn'] = table.player1_turn
        context['flop_card1'] = table.flop_card1
        context['flop_card2'] = table.flop_card2
        context['flop_card3'] = table.flop_card3
        context['pot_size'] = table.pot_size
        context['turn_card'] = table.turn_card
        context['river_card'] = table.river_card
        
    if table.player1 != "none" and table.player2 != "none" and table.error:
        context["reconnection"] = "yes"
        context["flop_displayed"] = table.flop_displayed
        context["turn_displayed"] = table.turn_displayed
        context["river_displayed"] = table.river_displayed
    else:
        context["reconnection"] = "no"
        
    context['dealer'] = table.dealer
    
    
    return render(request, 'poker/poker_room.html', context)

def path_does_not_exist(request):
    return render(request,"error_request.html")

def mobile_error(request):
    return render(request,"error_mobile.html")

def submit_request(request):
    if request.method == 'POST':
        #print(request.POST)
        form = SubmitRequestForm(request.POST)
        
        if form.is_valid():
            #print(request.POST)
            #print("here")
            try:
                #msg = EmailMessage('Request Callback', 'Here is the message.', to=['jkelly92@my.smccd.edu'])
                #msg.send()
                messages.add_message(request, messages.SUCCESS, 'Thanks for your submittion!')
                send_mail( escape(form.cleaned_data['subject']), escape(form.cleaned_data['from_email']) + "\n\n" + escape(form.cleaned_data['message']), 'letsplaypokermessages@gmail.com', ['letsplaypokermessages@gmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect("/")
        else:
            messages.add_message(request, messages.ERROR, 'Error in processing form data.')
            form = SubmitRequestForm()
            return render(request,"poker/request_submittion.html",{'form':form})
    
    form = SubmitRequestForm()
    return render(request, "poker/request_submittion.html", {"form": form})
