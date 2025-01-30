from django.conf import settings as conf
from bot import services as ser, buttons as btn 


def inline_button_handler(update, context):
    query = update.callback_query 
    user_id = query.from_user.id 
    
    if query.data == 'main_menu':
        context.bot.delete_message(chat_id = user_id, message_id=query.message.message_id)
        ser.main_menu(context, user_id)
    
    elif query.data == 'update':
        query.edit_message_reply_markup(
            reply_markup = btn.edit_data
        )
        
    elif query.data.startswith('edit'):
        edit = query.data.split('_')
        if edit[1]=='name':
            context.user_data['step'] = conf.STEPS['edit']['name']
            query.edit_message_text(text="Ism-Familiyangizni kiriting:")
        elif edit[1]=='number':
            context.user_data['step'] = conf.STEPS['edit']['phone_number']
            context.bot.delete_message(chat_id = user_id, message_id=query.message.message_id)
            ser.send_message(
                context = context, 
                chat_id = user_id, 
                text = "Quyidagi tugma orqali telefon raqamingizni ulashing: ",
                button = btn.share_contact
            )
        elif edit[1]=='study':
            context.user_data['step'] = conf.STEPS['edit']['study_place']
            query.edit_message_text(text="O'qish joyingiz nomini kiriting:")
        elif edit[1]=='group':
            context.user_data['step'] = conf.STEPS['edit']['study_group']
            query.edit_message_text(text="Guruhingizni kiriting:")
    
    elif query.data.startswith('back'):
        back = query.data.split('_')
        if back[-1] == 'data':
            context.bot.delete_message(chat_id = user_id, message_id= query.message.message_id)
            ser.send_user_info(context, user_id)
        
    