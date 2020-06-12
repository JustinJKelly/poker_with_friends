from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'base.html')