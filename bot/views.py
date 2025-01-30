from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from telegram import Update
from bot.main import bot, dispatcher  # main.py dan bot va dispatcher import qilinadi


@csrf_exempt
def telegram_webhook(request):
    """Telegram webhook view funksiyasi"""
    if request.method == "POST":
        try:
            update_data = json.loads(request.body)
            update = Update.de_json(update_data, bot)
            dispatcher.process_update(update)  # Yangilanishni qayta ishlash
            return JsonResponse({"status": "ok"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error"}, status=400)
    return JsonResponse({"status": "method not allowed"}, status=405)