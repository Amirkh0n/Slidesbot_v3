from modelapp.models import User 
from bot import services as ser, buttons as btn 


def send_user_info(context, user_id):
    context.user_data['step'] = 0
    msg = context.bot.send_message(
        chat_id = user_id, 
        text = "⏳",
        reply_markup = btn.ReplyKeyboardRemove()
    )
    context.bot.delete_message(chat_id = user_id,  message_id= msg.message_id)
    user = User.objects.get(user_id =user_id)
    text = f"""ㅤㅤㅤ📄 Ma'lumotlaringiz: 
👤Ism-Familiya: {user.info.full_name}
📞Nomer: {user.info.phone_number}
🎓O'qish joyi: {user.info.study_place}
👥Guruh: {user.info.study_group}"""
    
    ser.send_message(
        context = context, 
        chat_id = user_id, 
        text = text, 
        button = btn.user_info
    )