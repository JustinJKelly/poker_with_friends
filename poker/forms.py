from django import forms
from .models import Table

class MakeTableForm(forms.Form):
    #number_of_players = forms.CharField(label="Number of Players")
    starting_stack = forms.CharField(label="Starting Stack")
    big_blind = forms.CharField(label="Big Blind(small blind will be 1/2 BB)-Note: must be even integer")
    table_name = forms.CharField(label="Table Name")
    access_code = forms.CharField(label="Access Code")
    #decision_time = forms.IntegerField(label="Enter decision time(default=15s)")
    
class SubmitRequestForm(forms.Form):
    from_email = forms.EmailField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Enter email...', 'cols': '50', 'rows': '1',}))
    subject = forms.CharField(required=True, label="Subject", widget=forms.Textarea(attrs={'placeholder': 'Subject...', 'cols': '80', 'rows': '1',}))
    message = forms.CharField(required=True, label="Message", widget=forms.Textarea(attrs={'cols': '80', 'rows': '8', 'placeholder': 'Message...'}))
    
class JoinTableForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(JoinTableForm, self).__init__(*args,**kwargs)
        tables = Table.objects.all()
        self.fields['chosen_table'] = forms.ChoiceField(choices=[(table.table_id,table.table_name)for table in tables])
        self.fields['username'] = forms.CharField(label="Choose Username")
        self.fields['access_code'] = forms.CharField(label="Enter access code")
        #chosen_table = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='')
        
        
    
    