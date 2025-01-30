from django.urls import path
from bot.views import telegram_webhook

urlpatterns = [
    path("", telegram_webhook, name="telegram_webhook"),
]