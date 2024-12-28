from django.conf import settings
from bot import buttons as btn, services as ser
from modelapp.models import Message

def main_menu(context, chat_id):
    context.user_data['step']=settings.STEPS['main_menu']
    ser.send_message(
        context = context,
        chat_id = chat_id, 
        text = 'Asosiy Menu!',
        button = btn.main_menu
    )
