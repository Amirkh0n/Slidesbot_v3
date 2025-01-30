from bot import services as ser, buttons as btn 


def send_admin_panel(context, user_id):
    ser.send_message(
        context = context, 
        chat_id = user_id, 
        text = "Admin panelga xush kelibsiz! Kerakli bo'limni tanlang:",
        button = btn.admin_panel
    )