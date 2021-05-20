from ugc.models import Profile
from ugc.models import Message
from django.core.management.base import BaseCommand

import logging
from django.conf import settings

from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, chat
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,    
    CallbackContext,
    defaults
)
from telegram.utils.request import Request

logger = logging.getLogger(__name__)

def log_error(f):

    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Error: {e}'
            print(error_message)
            raise e
    return wrapper


@log_error
def do_echo(update: Update, contexr: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,    
        defaults={
            'name': update.message.from_user.username
        }    
    )
    
    m = Message(
        profile=p,
        text=text,
    )
    m.save()

    reply_text = f'{chat_id}\n\t {m.pk}: {text}'
    update.message.reply_text(
        text=reply_text
    )

@log_error
def do_count(update: Update, contexr: CallbackContext):
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user
        }
    )

    count = Message.objects.filter(profile=p).count()

    update.message.reply_text(
        text=f'message count: {count}'
    )

class Command(BaseCommand):
    help = 'tg-bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0
        )
        bot = Bot(
            request=request,
            token=settings.TG_TOKEN,
        )
        print(bot.get_me)

        updater = Updater (
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, do_echo)
        command_handler = CommandHandler('count', do_count)
        updater.dispatcher.add_handler(message_handler)
        updater.dispatcher.add_handler(command_handler)

        updater.start_polling()
        updater.idle()
