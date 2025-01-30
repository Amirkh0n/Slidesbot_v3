from django.conf import settings
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from bot import commands as comm, messages as msg, inlines as inl

bot = Bot(token=settings.TOKEN)
dispatcher = Dispatcher(bot, update_queue=None, workers=0)

# Handlerlarni qo‘shamiz
dispatcher.add_handler(CommandHandler('start', comm.start_command))
dispatcher.add_handler(CommandHandler('cancel', comm.cancel_command))

dispatcher.add_handler(MessageHandler(Filters.text, msg.handle_messages))
dispatcher.add_handler(MessageHandler(Filters.contact, msg.contact_handler))
dispatcher.add_handler(MessageHandler(Filters.photo, msg.photo_handler))
dispatcher.add_handler(MessageHandler(Filters.document, msg.file_handler))

dispatcher.add_handler(CallbackQueryHandler(inl.inline_button_handler))