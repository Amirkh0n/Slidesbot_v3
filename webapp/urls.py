from django.urls import path
from . import views

urlpatterns = [
    # dashboard 
    path('', views.dashboard, name="dashboard"),
    path('order-types/', views.order_types, name="order_types"),
    path('bot-settings/', views.bot_settings, name="settings"),
    
    # chat 
    path('users/', views.homepage, name="homepage"),
    path('send_file/', views.send_file, name='send_file'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_new_messages/', views.get_new_messages, name = "get_new_messages"),
    path('users/<int:user_id>/', views.chat, name="chat"),
]