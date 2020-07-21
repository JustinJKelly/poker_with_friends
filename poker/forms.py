from django import forms
#from .models import Table

class MakeTableForm(forms.Form):
    number_of_players = forms.CharField(label="Number of Players")
    starting_stack = forms.CharField(label="Starting Stack")
    big_blind = forms.CharField(label="Big Blind(small blind will be 1/2 BB)")
    table_name = forms.CharField(label="Table Name")
    decision_time = forms.IntegerField(label="Enter decision time(default=15s)")
    
class JoinTableForm(forms.Form):
    '''tables = Table.objects.all()
    CHOICES = []
    for table in tables:
        CHOICES.append( (table.table_id,table.table_name) )
    
    chosen_table = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='')'''
    username = forms.CharField(label="Choose Username")
    access_code = forms.CharField(label="Enter access code")
    
    