from modelapp.models import Message, Settings 



def send_message(context, chat_id, text, button=None):
    is_active = Settings.objects.all().first().is_active
    if is_active:
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
    

def send_photo(context, chat_id, photo, file_id, text = None, button=None):
    is_active = Settings.objects.all().first().is_active
    if is_active:
        msg = context.bot.send_photo(
            chat_id = chat_id,
            photo = photo,
            caption = text,
            reply_markup = button,
            parse_mode = 'HTML'
        )
        Message.objects.create(
            user_id = chat_id, 
            message_id = msg.message_id, 
            message_type = 'photo',
            file_id = file_id,
            message_text = text,
            from_chat = 'bot'
        )


def send_document(context, chat_id, document, file_id, text = None, button=None):
    is_active = Settings.objects.all().first().is_active
    if is_active:
        msg = context.bot.send_document(
            chat_id = chat_id,
            document = document,
            caption = text,
            reply_markup = button,
            parse_mode = 'HTML'
        )
        Message.objects.create(
            user_id = chat_id, 
            message_id = msg.message_id, 
            message_type = 'file',
            file_id = file_id,
            message_text = text,
            from_chat = 'bot'
        )