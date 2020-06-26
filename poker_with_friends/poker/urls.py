from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('make_table', views.make_table, name="make_table"),
    path('join_table', views.join_table, name="join_table"),
    path('table/<str:room_name>', views.room, name='room'),
]