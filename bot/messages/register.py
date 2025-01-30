from modelapp.models import User 
from django.conf import settings as conf
from bot import buttons as btn, services as ser



def regist_name(update, context):
    user_id = update.message.from_user.id
    user = User.objects.get(user_id = user_id)
    user.info.full_name = update.message.text
    user.info.save()
    if user.info.study_place is None:
        context.user_data['step']=conf.STEPS['regist']['study_place']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = "O'qish joyingiz nomini yozing! \nMasalan: Farg’ona Davlat Universiteti",
            button = btn.ReplyKeyboardRemove()
        )
        return
    elif user.info.study_group is None:
        context.user_data['step']=conf.STEPS['regist']['study_group']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = "Guruhingizni yozib qoldiring! \nMasalan: 19.112-guruh",
            button = btn.ReplyKeyboardRemove()
        )
        return
    elif user.info.phone_number is None:
        context.user_data['step']=conf.STEPS['regist']['phone_number']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = "Pastdagi tugma orqali telefon raqamingizni ulashing:",
            button = btn.share_contact
        )
        return
    elif context.user_data.get('step', 0)==conf.STEPS['edit']['name']:
        ser.send_user_info(context, user_id)
        return 
        
    ser.main_menu(context=context, chat_id = user_id)


def regist_study_place(update, context):
    user_id = update.message.from_user.id
    user = User.objects.get(user_id = user_id)
    user.info.study_place = update.message.text
    user.info.save()
    if user.info.study_group is None:
        context.user_data['step']=conf.STEPS['regist']['study_group']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = "Guruhingizni yozib qoldiring! \nMasalan: 19.112-guruh",
            button = btn.ReplyKeyboardRemove()
        )
        return
    elif user.info.phone_number is None:
        context.user_data['step']=conf.STEPS['regist']['phone_number']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = "Pastdagi tugma orqali telefon raqamingizni ulashing:",
            button = btn.share_contact
        )
        return
    elif context.user_data.get('step', 0)==conf.STEPS['edit']['study_place']:
        ser.send_user_info(context, user_id)
        return
    
    ser.main_menu(context=context, chat_id = user_id)


def regist_study_group(update, context):
    user_id = update.message.from_user.id
    user = User.objects.get(user_id = user_id)
    user.info.study_group = update.message.text
    user.info.save()
    if user.info.phone_number is None:
        context.user_data['step']=conf.STEPS['regist']['phone_number']
        ser.send_message(
            context = context, 
            chat_id = user_id, 
            text = "Pastdagi tugma orqali telefon raqamingizni ulashing:",
            button = btn.share_contact
        )
        return
    elif context.user_data.get('step', 0)==conf.STEPS['edit']['study_group']:
        ser.send_user_info(context, user_id)
        return
    ser.main_menu(context=context, chat_id = user_id)
