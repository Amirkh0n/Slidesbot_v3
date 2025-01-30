from django.conf import settings
from bot import buttons as btn, services as ser
from modelapp.models import Message, User

def main_menu(context, chat_id):
    admins = User.objects.filter(is_admin = True)
    admins_id = [admin.user_id for admin in admins]
    button = btn.main_menu(is_admin = True) if chat_id in admins_id else btn.main_menu(is_admin = False)
    context.user_data['step']=settings.STEPS['main_menu']
    ser.send_message(
        context = context,
        chat_id = chat_id, 
        text = 'Asosiy Menu!',
        button = button
    )
