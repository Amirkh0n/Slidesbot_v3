from django.shortcuts import render, get_object_or_404 
from modelapp.models import User, Message
from django.db.models import Max
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from bot.main import bot

from django.db.models import OuterRef, Subquery


# Create your views here.
def homepage(request):
    now = timezone.now()
    ranges = range(100)
    users = (
        User.objects.prefetch_related('messages')
        .annotate(latest_message_id=Max('messages__id'))
        .order_by('-latest_message_id')
    )
    return render(request, 'chat/homepage.html', {'users': users, 'now': now, 'ranges': ranges})


def chat(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    messages = user.messages.filter(user_id=user_id)
    
    return render(request, 'chat/user_chat.html', {'user': user, 'messages' : messages })
    


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        message_text = data.get('message_text')
        
        message_ = bot.send_message(
            chat_id = user_id, 
            text = message_text 
        )
        
        # Xabarni saqlash
        new_message = Message.objects.create(
            user_id=user_id,
            message_text=message_text,
            from_chat='bot'  # Yoki kerakli qiymat
        )

        # Javob sifatida yangi xabar ma'lumotlarini qaytarish
        return JsonResponse({
            'id': new_message.id,
            'message_text': new_message.message_text,
            'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'from_chat': new_message.from_chat,
        })
    return JsonResponse({'error': 'Faqat POST so‘rovlariga ruxsat berilgan'}, status=400)
    

def get_new_messages(request):
    last_message_id = request.GET.get('last_message_id')
    user_id = request.GET.get('user_id')  # Foydalanuvchi ID sini olish

    # Foydalanuvchiga mos xabarlarni olish
    messages = Message.objects.filter(user_id=user_id, id__gt=last_message_id).order_by('created_at')

    # Xabarlar bo'lsa, ularni qaytarish
    messages_data = [{
        'id': message.id,
        'message_text': message.message_text,
        'from_chat': message.from_chat,
        'created_at': message.created_at.isoformat()  # DateTime formatni o'zgaritish
    } for message in messages]

    return JsonResponse({'messages': messages_data})