from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    #path('make_table', views.make_table, name="make_table"),
    path('join_table', views.join_table, name="join_table"),
    path('make_table', views.make_table, name="make_table"),
    path('submit_request', views.submit_request, name='submit_request'),
    path('table/<str:room_name>', views.room, name='room'),
    path('table/<str:table_id>/<str:room_name>', views.room_protected, name='room_protected'),
    path('mobile_error', views.mobile_error, name='mobile_error'),
    re_path(r'^.*/$',views.path_does_not_exist, name="path_dne")
]