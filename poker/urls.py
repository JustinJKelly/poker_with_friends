from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    #path('make_table', views.make_table, name="make_table"),
    path('join_table', views.join_table, name="join_table"),
    path('table/<str:room_name>', views.room, name='room'),
    path('table/<str:table_id>/<str:room_name>', views.room_protected, name='room_protected'),
    re_path(r'^.*/$',views.path_does_not_exist, name="path_dne")
]