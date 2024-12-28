from django.contrib import admin
from .models import User, UserInfo, Order, OrderType, Message
# Register your models here.

admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(Order)
admin.site.register(OrderType)
admin.site.register(Message)