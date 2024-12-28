from modelapp.models import User, UserInfo

def get_or_create_user(user_id, first_name, username):
    user  = User.objects.get_or_create(
        user_id=user_id,
        defaults={
            'first_name': first_name,
            'username': username,
        }
    )
    
    if user[1]:
        UserInfo.objects.get_or_create(
            user_id = user_id
        )
    
    return user