import logging
import config

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,    
    CallbackContext
)

logger = logging.getLogger(__name__)

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
        return ConversationHandler.END
    elif answer == 'no':
        logger.info(f"restart registration {username}")
        update.message.reply_text('Lets start over. What is your name?')
        return LOGIN
    else:
        logger.info(f"unhandled command {username}")
        update.message.reply_text('just say yes or no')
        return CHECK
    
def cancel(update: Update, context : CallbackContext) -> int:
    user = update.message.from_user
    username = context.user_data[user]
    logger.info(f"User {username} canceled the conversation.")
    update.message.reply_text(
        'Bye!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:    
    updater = Updater(config.TG_TOKEN)    
    dispatcher = updater.dispatcher    
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

    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()    
    updater.idle()

if __name__ == '__main__':
    main()