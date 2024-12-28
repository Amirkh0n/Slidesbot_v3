from modelapp.models import Message 


def send_message(context, chat_id, text, button=None):
    msg = context.bot.send_message(
        chat_id = chat_id, 
        text = text,
        reply_markup = button,
        parse_mode = 'HTML'
    )
    Message.objects.create(
        user_id = chat_id, 
        message_id = msg.message_id, 
        message_type = 'text',
        message_text = text,
        from_chat = 'bot'
    )
    