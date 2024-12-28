import requests
from django.conf import settings as conf 


def download_file(file_id):
    bot_token = conf.TOKEN
    # Telegram API orqali fayl ma'lumotlarini olish
    file_info_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
    file_info = requests.get(file_info_url).json()

    # Yuklab olish uchun URL
    file_path = file_info['result']['file_path']
    
    return f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
