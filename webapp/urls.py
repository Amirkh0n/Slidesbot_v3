from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('send_message/', views.send_message, name='send_message'),
    path('get_new_messages/', views.get_new_messages, name = "get_new_messages"),
    path('users/<int:user_id>', views.chat, name="chat")
]