from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MakeTableForm, JoinTableForm
from django.contrib import messages
from .models import Table

# Create your views here.
def make_table(request):
    if request.method == 'POST':
        #print(request.POST)
        form = MakeTableForm(request.POST)
        if form.is_valid():
            print(request.POST)
        else:
            messages.add_message(request, messages.ERROR, 'Error in processing form data')
            form = MakeTableForm()
            return render(request,"poker/make_table.html",{'form':form})
        #return HttpResponse("Thanks")
    
    form = MakeTableForm()
    return render(request, "poker/make_table.html", {"form": form})

# Create your views here.
def join_table(request):
    if request.method == 'POST':
        form = JoinTableForm(request.POST)
        if form.is_valid():
            print(request.POST['chosen_table'])
            print(request.POST['access_code'])
            print(request.POST['username'])
            table = Table.objects.get(table_id=request.POST['chosen_table'])
            if request.POST['access_code'] == table.access_code:
                redirect = HttpResponseRedirect("/poker/table/"+table.table_name)
                request.session['username'] = request.POST['username']
                return redirect
            else:
                messages.add_message(request, messages.ERROR, 'Error in processing form data')
                form = JoinTableForm()
                return render(request,"poker/join_table.html",{'form':form})
        else:
            messages.add_message(request, messages.ERROR, 'Error in processing form data')
            form = JoinTableForm()
            return render(request,"poker/join_table.html",{'form':form})

    form = JoinTableForm()
    return render(request, "poker/join_table.html", {"form": form})

def room(request, room_name):
    username= request.session.get('username')
    return render(request, 'poker/room.html', {
        'room_name': room_name, 'username':username
    })