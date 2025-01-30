from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import time 
import requests
from django.conf import settings as conf 


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=35, null=True, blank=True)
    first_name = models.CharField(max_length=35)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    
    def __str__(self):
        return self.first_name


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="info")  # user_id bilan bog'lanish
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    study_place = models.CharField(max_length=100, null=True, blank=True)
    study_group = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name or self.user.first_name
        

class OrderType(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.name} - {self.price} so'm"

# Buyurtmalar jadvali modeli
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    order_type = models.ForeignKey(OrderType, on_delete=models.CASCADE, related_name="type")
    subject = models.CharField(max_length=255, null=True, blank=True)
    theme = models.TextField(null=True,  blank=True)  # Buyurtma haqida batafsil ma'lumot
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.first_name} - {self.order_type.name} ({self.theme})" 


class Message(models.Model):
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('photo', 'Photo'),
        ('file', 'File'),
    ]

    FROM_CHAT_CHOICES = [
        ('bot', 'Bot'),
        ('user', 'User'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message_id = models.IntegerField(null=True, blank=True)  # Telegram message_id
    message_type = models.CharField(max_length=10, default='text', choices=MESSAGE_TYPES)
    message_text = models.TextField(blank=True, null=True)
    file_id = models.CharField(max_length=255, null=True, blank=True)
    from_chat = models.CharField(max_length=10, choices=FROM_CHAT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_file_url(self):
        if self.file_id:
            #time.sleep(0.5)
            bot_token = conf.TOKEN
            # Telegram API orqali fayl ma'lumotlarini olish
            file_info_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={self.file_id}"
            file_info = requests.get(file_info_url).json()
            # Yuklab olish uchun URL
            file_path = file_info['result']['file_path']
            return f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
    
    def __str__(self):
        return f"{self.get_from_chat_display()}({self.get_message_type_display()})"
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'id']),  # Indeks yaratish
        ]
        

class Settings(models.Model):
    web_app = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Web App: {self.web_app}, Active: {self.is_active}"