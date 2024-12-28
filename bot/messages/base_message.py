from django.conf import settings as conf
from modelapp.models import User, Message, OrderType, Order
from bot import buttons as btn, services as ser
import bot

def handle_messages(update, context):
    user_id = update.message.from_user.id
    message = update.message.text 
    step = context.user_data.get('step', 0)
    user, created = user, created = ser.get_or_create_user(user_id, update.message.from_user.first_name, update.message.from_user.username)
    
    Message.objects.create(
        message_id = update.message.message_id,
        user = user, 
        message_type = 'text',
        message_text = message, 
        from_chat = "user"
    )
    
    if message == 'Buyurtma':
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = "Nima buyurtma qilmoqchisiz?",
            button = btn.orders()
        )
    
    elif message == 'Ma\'lumotlarim':
        pass
    
    elif message in [order.name for order in OrderType.objects.all()]:
        order_type = OrderType.objects.get(name = message)
        context.user_data['order'] = Order.objects.create(user = user, order_type = order_type)
        context.user_data['step'] = conf.STEPS['order']['subject']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = "Fan nomini kiriting:", 
            button = btn.ReplyKeyboardRemove()
        )
        
    elif message == "Orqaga 🔙":
        pass
    
    elif step == conf.STEPS['order']['subject']:
        order = context.user_data.get('order')
        order.subject = message
        order.save()
        context.user_data['step'] = conf.STEPS['order']['theme']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = f"{order.order_type.name}ning mavzusini kiriting:"
        )
    
    elif step == conf.STEPS['order']['theme']:
        order = context.user_data.get('order')
        order.theme = message
        order.status = 'in_progress'
        order.save()
        context.user_data['step'] = conf.STEPS['order']['theme']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = f"Buyurtmangizni tayyorlashimiz uchun quyidagi karta raqamiga {order.order_type.price : ,} so'm to'lov qilib, chekini screenshot qilib rasm ko'rinishida jo'natishingiz kerak bo'ladi!!!\n"
                      "<pre>9860 1601 2673 3114</pre>(Fazliddin Turg’unboev)\n\n"
                      "Buyurtmani bekor qilish uchun👉 /start 👈ni bosing!"
        )
    
    elif step == conf.STEPS['regist']['name']:
        bot.messages.register.regist_name(update, context)
    
    elif step == conf.STEPS['regist']['study_place']:
        bot.messages.register.regist_study_place(update, context)
    
    elif step == conf.STEPS['regist']['study_group']:
        bot.messages.register.regist_study_group(update, context)
    

def contact_handler(update, context):
    user_id = update.message.from_user.id
    number = f"+{update.message.contact.phone_number}"
    Message.objects.create(
        message_id = update.message.message_id,
        user_id = user_id, 
        message_type = 'text',
        message_text = number, 
        from_chat = "user"
    )
    if context.user_data.get('step', 0) == conf.STEPS['regist']['phone_number']:
        user = User.objects.get(user_id = user_id)
        user.info.phone_number = number
        user.info.save()
        ser.main_menu(context, user_id)