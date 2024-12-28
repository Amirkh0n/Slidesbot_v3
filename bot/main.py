from django.conf import settings
from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters, 
#    CallbackQueryHandler
)
from bot import commands as comm, messages as msg 

updater=Updater(token=settings.TOKEN)
bot = updater.bot

def main():
    
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start', comm.start_command))
    dp.add_handler(MessageHandler(Filters.text, msg.handle_messages))
    dp.add_handler(MessageHandler(Filters.contact, msg.contact_handler))
    dp.add_handler(MessageHandler(Filters.photo, msg.photo_handler ))
    dp.add_handler(MessageHandler(Filters.document, msg.file_handler))
    
    updater.start_polling()
    print("""\t★★★Running bot!!!★★★
》》》to stop -> CTRL + C《《《
""")
    updater.idle()
    print('\t•••STOPPED!!!•••')

