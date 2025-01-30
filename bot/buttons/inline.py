from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from modelapp.models import Settings 


def url():
    return Settings.objects.all().first().web_app
    
    
def user_url(user_id):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(
            text="📞 Bog'lanish",  
            url = f"{url()}/users/{user_id}"
        )]]
    )

    
user_info = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="Tahrirlash 🖋", callback_data = "update")], 
        [InlineKeyboardButton(text="Asosiy Menu",  callback_data="main_menu")]
    ]
)

edit_data = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text='Ism-Familiya', callback_data='edit_name'), InlineKeyboardButton(text='Nomer', callback_data='edit_number')],
        [InlineKeyboardButton(text="O'qish joyi", callback_data='edit_study'), InlineKeyboardButton(text='Guruh', callback_data='edit_group')],
        [InlineKeyboardButton(text='Orqaga 🔙', callback_data='back_to_user_data')]
    ]
)


admin_panel = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="Reklama yuborish 💰", callback_data="adds")],
        [InlineKeyboardButton(text="Admin App", url = url())]
    ]
)