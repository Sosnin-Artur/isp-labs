
from telegram import (
    Bot,
    Update,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler,
    ConversationHandler,
    CallbackContext,
)

from dtb.settings import TELEGRAM_TOKEN

from tgbot.models import User
import logging

logger = logging.getLogger(__name__)

def create(update: Update, context : CallbackContext):    
    if User.create_user(update, context) is not None:
        return True
    return False

LOGIN, LOCATION, BIO, CHECK = range(4)

def start(update: Update, context : CallbackContext) -> int:    
    user = update.message.from_user
    logger.info(f"{user.username} start")
    update.message.reply_text(
        'Hi! What is your name? ',
        reply_markup=ReplyKeyboardRemove()
    )

    return LOGIN

def login(update: Update, context : CallbackContext) -> int:    
    user = update.message.from_user
    username = context.user_data[user] = update.message.text
    logger.info(f"username: {username}")
    update.message.reply_text(
        f'Nice to meet you {username}, please send me your location'
    )

    return LOCATION

def location(update: Update, context : CallbackContext) -> int:    
    user = update.message.from_user
    username = context.user_data[user]
    user_location = update.message.text
    logger.info(f"Location of {username}: {user_location}")
    update.message.reply_text(
        'See you soon 😈😈😈😈😈😈😈😈😈😈'
    )
    update.message.reply_text("I'm shure that you want say something about yourself")

    return BIO

def skip_location(update: Update, context : CallbackContext) -> int:
    user = update.message.from_user
    username = context.user_data[user]
    logger.info(f"User { username} did not send a location.")
    update.message.reply_text(
        'Oh. Ok.....'
    )
    update.message.reply_text("I'm shure that you want say something about yourself")

    return BIO

def bio(update: Update, context : CallbackContext) -> int:    
    reply_keyboard = [['yes', 'no']]
    
    user = update.message.from_user
    username = context.user_data[user]
    location = update.message.text
    logger.info(f"Bio of {username}: {location}")
    update.message.reply_text(f'{username} : {location}. correct?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)

    return CHECK

def check(update: Update, context : CallbackContext) -> int:
    user = update.message.from_user
    username = context.user_data[user]
    answer = update.message.text
    if answer == 'yes':
        logger.info(f"end registration {username}")
        update.message.reply_text('Now we can say goodbye', reply_markup=ReplyKeyboardRemove())    
        if create(update, context):
            update.message.reply_text('creations seccssessful')    
            return ConversationHandler.END
        else:
            update.message.reply_text('username is busy, please try another.What is your name?')
            return LOGIN    
    elif answer == 'no':    
        logger.info(f"restart re")
        update.message.reply_text('')
        return LOGIN      
    else:
        logger.info(f"unhandled command {username}")
        update.message.reply_text('just say yes or no')
        return CHECK
    
def cancel(update: Update, context : CallbackContext) -> int:
    user = update.message.from_user
    username = context.user_data[user]
    logger.info(f"User {username} canceled the Registration.")
    update.message.reply_text(
        'Bye!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

