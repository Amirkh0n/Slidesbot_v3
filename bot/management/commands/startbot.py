from django.core.management.base import BaseCommand
from bot.main import main

class Command(BaseCommand):
    help = "Telegram botni ishga tushiradi."

    def handle(self, *args, **kwargs):
        self.stdout.write("Bot ishga tushdi...")
        main()
