from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from modelapp.models import OrderType 


def main_menu(is_admin = False):
    button = [
        [
            KeyboardButton(text="Buyurtma"), 
            KeyboardButton(text="Ma'lumotlarim")
        ]
    ]
    if is_admin == True: 
        button.append([KeyboardButton(text="Admin panel 🔐")])
    return ReplyKeyboardMarkup(button, resize_keyboard=True)

share_contact = ReplyKeyboardMarkup([
    [KeyboardButton(text='Ulashish 📞', request_contact=True)]
], resize_keyboard=True)

def orders():
    orders = OrderType.objects.all()
    buttons = []
    for order in orders:
        buttons.append(KeyboardButton(text = order.name))
    return ReplyKeyboardMarkup(
        [buttons[i: i+2] for i in range(0, len(buttons), 2)]+[[KeyboardButton(text="Orqaga 🔙")]],
        resize_keyboard = True 
    )
     