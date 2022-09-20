from django.urls import path
from . import views
app_name='chat'

urlpatterns = [
    path('', views.show_chats, name = 'show_chats'),
    path('get_last_msg/', views.get_last_msg, name = 'get_last_msg'),
    path('search_chats/', views.search_chats, name = 'search_chats'),

    path('workers_list/', views.workers_list, name='workers_list'),
    path('workers_list_a/<str:slug>/', views.workers_list_a, name='workers_list_a'),

    path('add_worker/', views.add_worker, name='add_worker'),
    path('<str:room>/', views.room, name='room'),
    path('checkview/', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]