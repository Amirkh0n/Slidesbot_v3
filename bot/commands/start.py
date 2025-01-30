from modelapp.models import User, Message
from bot import buttons as btn, services as ser
from django.conf import settings as conf
    
def start_command(update, context):
    context.user_data['step'] = conf.STEPS['main_menu']
    user_id = update.message.from_user.id
    user, created = ser.get_or_create_user(user_id, update.message.from_user.first_name, update.message.from_user.username)
    
    Message.objects.create(
        message_id = update.message.message_id,
        user_id = user_id, 
        message_type = 'text',
        message_text = update.message.text, 
        from_chat = "user"
    )
    
    if created or user.info.phone_number is None:
        context.user_data['step']=conf.STEPS['regist']['name']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text="Assalom aleykum, Mustaqil ishlar uchun slaytlar, maqolalar va tezislar hamda kurs ishi yozib beramiz. \n"
                 "Batafsil ma'lumot: /info \n\nBotdan foydalanish uchun ism familiyangizni yozing.\n\n"
                 "(Misol: Abdulloh Akbaraliyev)\n\t❗❗❗❗❗❗❗❗❗❗❗❗\n"
                 "(Iltimos fake ma'lumotlar bermang, har bir buyurtma adminlar tomonidan tekshiriladi!)",
            button = btn.ReplyKeyboardRemove()
        )
        return 
    
    else:
        if user.is_active == False:
            user.is_active = True 
            user.save()
        ser.main_menu(context, user_id)
    