from os import name
from ugc.models import Profile
from django.core.management.base import BaseCommand

import logging
from django.conf import settings

from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, chat, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,    
    CallbackContext,
    defaults,
    CallbackQueryHandler
)
from telegram.utils.request import Request

from .validators import GENDER_MAP
from .validators import gender_hru
from .validators import validate_age

logger = logging.getLogger(__name__)

def debug_requests(f):

    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Error: {e}'
            print(error_message)
            raise e
    return wrapper

logger = logging.getLogger(__name__)

# CRUD
# create
def add_user(update: Update, context: CallbackContext):    
    if Profile.objects.get(name=context.user_data['name']):
        return False
    else:
        Profile.objects.create(name=context.user_data['name'],
                            location=context.user_data['location'],
                            bio=context.user_data['bio'])
        return True
# read
def get_user(update: Update, context: CallbackContext):    
    user = Profile.objects.get(name=context.user_data['name'])
    if user:
        return user
    else:        
        update.message.reply_text(
            'no such user'
        )
        return None

def get_all_users(update: Update, context: CallbackContext):    
    return Profile.objects.all()

# update
def update_user(update: Update, context: CallbackContext):   
    CHANGE_MAP = {
        1: 'name',
        2: 'location',
        3: 'bio',
    }

    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=value, callback_data=key) for key, value in CHANGE_MAP.items()],
        ],
    )
    update.message.reply_text(
        text='choice change paramenter',
        reply_markup=inline_buttons,
    )
    choice = update.callback_query.data
    choice = int(choice)

    update.message.reply_text(
        text='new value',        
    )
    val = update.message.text

    Profile.objects.filter(name=context.user_data['name']).update(**(CHANGE_MAP[choice],val))

# delete
def delete_user(update: Update, context: CallbackContext):    
    Profile.objects.filter(name=context.user_data['name']).delete()

LOGIN, LOCATION, BIO, CHECK = range(4)

def start(update: Update, context : CallbackContext):    
    user = update.message.from_user
    logger.info(f"{user.username} start")
    update.message.reply_text(
        'Hi! What is your name? ',
        reply_markup=ReplyKeyboardRemove()
    )

    return LOGIN

def login(update: Update, context : CallbackContext):    
    user = update.message.from_user
    username = context.user_data['name'] = update.message.text
    logger.info(f"username: {username}")
    update.message.reply_text(
        f'Nice to meet you {username}, please send me your location'
    )

    return LOCATION

def location(update: Update, context : CallbackContext):    
    user = update.message.from_user
    username = context.user_data['name']
    context.user_data['location'] = user_location = update.message.text
    logger.info(f"Location of {username}: {user_location}")
    update.message.reply_text(
        'See you soon 😈😈😈😈😈😈😈😈😈😈'
    )
    update.message.reply_text("I'm shure that you want say something about yourself")

    return BIO

def skip_location(update: Update, context : CallbackContext):
    user = update.message.from_user
    username = context.user_data['name']
    logger.info(f"User {username} did not send a location.")
    update.message.reply_text(
        'Oh. Ok.....'
    )
    update.message.reply_text("I'm shure that you want say something about yourself")

    return BIO

def bio(update: Update, context : CallbackContext):    
    reply_keyboard = [['yes', 'no']]
    
    user = update.message.from_user
    username = context.user_data['name']
    context.user_data['bio'] = bio = update.message.text
    logger.info(f"Bio of {username}: {bio}")
    update.message.reply_text(f'{username} : {bio}. correct?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)

    return CHECK

def check(update: Update, context : CallbackContext):
    user = update.message.from_user
    username = context.user_data['name']
    answer = update.message.text
    if answer == 'yes':
        logger.info(f"end registration {username}")
        if add_user(update, context):            
            return ConversationHandler.END
        else:            
            update.message.reply_text('sorry but this username is busy, select another, please')    
            return LOGIN    
    elif answer == 'no':
        logger.info(f"restart registration {username}")
        update.message.reply_text('Lets start over. What is your name?')
        return LOGIN
    else:
        logger.info(f"unhandled command {username}")
        update.message.reply_text('just say yes or no')
        return CHECK
    
def cancel(update: Update, context : CallbackContext):
    user = update.message.from_user
    username = context.user_data['name']
    logger.info(f"User {username} canceled the conversation.")
    update.message.reply_text(
        'Bye!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def help(update: Update, context : CallbackContext):
    update.message.reply_text('print /start')


class Command(BaseCommand):
    help = 'tg-bot'

    def handle(self, *args, **options):
        logger.info('Started Anketa-bot')

        req = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            token=settings.TG_TOKEN,
            request=req,            
        )
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        # Проверить что бот корректно подключился к Telegram API
        info = bot.get_me()
        logger.info(f'Bot info: {info}')

        # Навесить обработчики команд
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={            
                LOGIN: [MessageHandler(Filters.text, login)],            
                LOCATION: [
                    MessageHandler(Filters.text, location),
                    CommandHandler('skip', skip_location),
                ],           
                BIO: [MessageHandler(Filters.text, bio)],
                CHECK: [MessageHandler(Filters.text , check),],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
        updater.dispatcher.add_handler(conv_handler)
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(Filters.all, help))

        # Начать бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
        logger.info('Stopped Anketa-bot')
