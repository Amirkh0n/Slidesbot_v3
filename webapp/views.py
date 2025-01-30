from django.shortcuts import render, get_object_or_404 
from modelapp.models import User, Message
from django.db.models import Max
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from bot.main import bot
from bot.services import download_file

from django.db.models import OuterRef, Subquery
from django.core.serializers import serialize


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
    msg_len = len(messages)
    start = msg_len-100 if msg_len>100 else 0
    msg = messages[start:msg_len]
    return render(request, 'chat/user_chat.html', {'user': user, 'messages' : msg, 'len_msg': msg_len})
    


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
            message_id = message_.message_id, 
            message_text=message_text,
            from_chat='bot'  # Yoki kerakli qiymat
        )

        # Javob sifatida yangi xabar ma'lumotlarini qaytarish
        return JsonResponse({
            'id': new_message.id,
            'message_text': new_message.message_text,
            'created_at': new_message.created_at.strftime('%m-%d %H:%M'),
            'from_chat': new_message.from_chat,
        })
    return JsonResponse({'error': 'Faqat POST so‘rovlariga ruxsat berilgan'}, status=400)

@csrf_exempt
def send_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        message_id = data.get('message_text')
        file_id = data.get('file_id')
        
        new_message = Message.objects.create(
            user_id=user_id,
            message_id = message_id, 
            file_id =file_id,
            message_type = 'file',
            from_chat='bot'  # Yoki kerakli qiymat
        )
        return JsonResponse({
            'id': new_message.id,
            'file_id': new_message.file_id,
            'get_file_url': new_message.get_file_url(),
            'created_at': new_message.created_at,
            'from_chat': new_message.from_chat,
        })




def get_new_messages(request):
   # try:
        # So'rovdan ma'lumotlarni olish
        old_len = int(request.GET.get('len_msg', 0))
        user_id = request.GET.get('user_id')

        # Parametrlarning mavjudligini tekshirish
        if not user_id:
            return JsonResponse({'error': 'Missing user_id parameter'}, status=400)

        # Foydalanuvchiga mos keluvchi xabarlarni olish
        messages = Message.objects.filter(user_id=user_id).order_by('created_at')
        new_len = len(messages)
        
        print(old_len, new_len)
        # Faqat yangi xabarlarni olish
        if old_len < new_len:
            new_messages = messages[old_len:new_len]
            have_new = True
        else:
            new_messages = []
            have_new = False 
        # Xabarlarni serializatsiya qilish
        data = []
        for msg in new_messages:
            data.append(
                {
                    'fields': {
                        "message_id": msg.message_id, 
                        "message_type": msg.message_type,
                        "message_text": msg.message_text,
                        "from_chat": msg.from_chat,
                        "created_at": msg.created_at,
                        "get_file_url": msg.get_file_url()
                    }
                }
            )
        #messages_json = serialize('json', new_messages)
        return JsonResponse({'messages': data, 'have_new': have_new}, safe=False)

    #except Exception as e:
#        return JsonResponse({'error': str(e)}, status=500)
    