from django.conf import settings as conf 
import bot.services as ser
import bot.buttons as btn
from modelapp.models import Message, User, Order

def photo_handler(update, context):
    step = context.user_data.get('step', 0)
    user_id = update.message.from_user.id 
    
    photo = update.message.photo[-1]
    file_id = photo.file_id 
    #photo_url = ser.download_file(file_id)
    
    message = Message.objects.create(
        user_id = user_id, 
        message_id = update.message.message_id, 
        message_type = 'photo',
        file_id = file_id, 
        from_chat = 'user'      
    )
    
    if step == conf.STEPS['order']['check']:
        admins = User.objects.filter(is_admin=True)
        order = context.user_data.get('order', Order.objects.order_by('-id').first())
        order.status = 'completed'
        order.save()
        for admin in admins:
            ser.send_photo(
                context = context, 
                chat_id = admin.user_id,
                photo = photo, 
                file_id = file_id, 
                button = btn.user_url(user_id),
                text = f"""ㅤㅤㅤ🌟<b>Yangi buyurtma:</b> 
👤<b>User:</b> {order.user.info.full_name}
📞<b>Nomer:</b> {order.user.info.phone_number}
🎓<b>O'qish joyi:</b> {order.user.info.study_place}
👥<b>Guruhi:</b> {order.user.info.study_group}
📤<b>Buyurtma:</b> {order.order_type.name}
📚<b>Fan:</b> {order.subject}
📃<b>Mavzu:</b> {order.theme}"""
            )
        
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = "Hurmatli mijoz buyurtmangiz qabul qilindi. Buyurtma 24-72 soat ichida tayyor bo'ladi. Tez orada adminimiz siz bilan bog'lanishadi!"
        )
        del context.user_data['order']
        ser.main_menu(context, user_id)