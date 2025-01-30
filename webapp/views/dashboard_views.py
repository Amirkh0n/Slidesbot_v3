from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now, make_aware
from modelapp.models import User, Order, OrderType, Settings

def dashboard(request):
    # Foydalanuvchilar statistikasi
    all_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    # OrderType 
    order_type = OrderType.objects.count()
    
    # Umumiy daromad (status = "completed")
    income = Order.objects.filter(status="completed").aggregate(
        total_price=Sum('order_type__price')
    )['total_price'] or 0  # Agar None bo'lsa, 0 qaytaradi

    # Hozirgi sana
    today = now()
    
    # Hozirgi oyning birinchi va oxirgi sanasi
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Hozirgi oyda bajarilgan buyurtmalarning daromadi
    current_month_income = Order.objects.filter(
        status="completed",
        created_at__gte=first_day_of_month,
        created_at__lte=last_day_of_month
    ).aggregate(total_income=Sum('order_type__price'))['total_income'] or 0

    # Hozirgi oy nomi
    current_month = today.strftime("%B")
    
    # Ma'lumotlarni kontekstga tayyorlash
    context = {
        'all_users': all_users,
        'active_users': active_users,
        'income': income,
        'monthly_income': current_month_income,
        'month': current_month,
        'order_type': order_type,
        'settings': Settings.objects.all().first()
    }

    return render(request, "dashboard/dash.html", context)


def order_types(request):
    # GET - Ro'yxatni ko'rsatish
    if request.method == "GET":
        order_types = OrderType.objects.all()
        return render(request, 'dashboard/order_type.html', {'order_types': order_types})

    # POST - Yaratish va Yangilash
    if request.method == "POST":
        if 'create' in request.POST:  # Yaratish uchun
            name = request.POST.get('name')
            price = request.POST.get('price')
            OrderType.objects.create(name=name, price=price)
            return redirect('order_types')

        elif 'update' in request.POST:  # Yangilash uchun
            obj_id = request.POST.get('id')
            order_type = get_object_or_404(OrderType, id=obj_id)
            order_type.name = request.POST.get('name')
            order_type.price = request.POST.get('price')
            order_type.save()
            return redirect('order_types')

    # DELETE - O'chirish
    if request.method == "POST" and '_method' in request.POST and request.POST['_method'] == 'DELETE':
        obj_id = request.POST.get('id')
        order_type = get_object_or_404(OrderType, id=obj_id)
        order_type.delete()
        return redirect('order_types')


def bot_settings(request):
    # GET - Ro'yxatni ko'rsatish
    if request.method == "GET":
        settings = Settings.objects.all().first()
        return render(request, 'dashboard/bot_settings.html', {'settings': settings})
    
    elif 'update' in request.POST:  # Yangilash uchun
            obj_id = request.POST.get('id')
            settings = get_object_or_404(Settings, id=obj_id)
            settings.web_app = request.POST.get('web_app')
            is_active = True if request.POST.get('is_active') == 'on' else False
            settings.is_active = is_active
            settings.save()
            return redirect("settings")
    
