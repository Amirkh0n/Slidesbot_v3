from bot import services as ser
from modelapp.models import Message 

def cancel_command(update, context):
    Message.objects.create(
        message_id = update.message.message_id,
        user_id = update.message.from_user.id, 
        message_type = 'text',
        message_text = update.message.text, 
        from_chat = "user"
    )
    order = context.user_data.get('order')
    try:
        order.status = 'canceled'
        order.save()
        del context.user_data['order']
    except:
        pass
    
    ser.main_menu(context, update.message.from_user.id)