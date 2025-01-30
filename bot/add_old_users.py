#from bot.main import bot 
import json 
from modelapp.models import User, UserInfo 

def add_json_user(bot):
    no_user = 0
    with open('bot/slides_data.json', 'r') as file:
        data = json.load(file)
    users_id=list(data.keys())
    for user_id in users_id:
        try:
            user = bot.get_chat(chat_id=int(user_id))
            is_active = True if user.photo else False 
            User.objects.create(
                user_id = int(user_id),
                name = user.first_name,
                is_active = is_active 
            )
            UserInfo.objects.create(
                user_id = int(user_id)
            )
        except: 
            no_user += 1
        
    print("No users: ", no_user)