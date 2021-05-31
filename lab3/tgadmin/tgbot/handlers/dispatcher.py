"""
    Telegram event handlers
"""

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

from tgbot.handlers import admin, commands, files
from tgbot.handlers.commands import broadcast_command_with_message
from tgbot.handlers.static_text import broadcast_command
from tgbot.handlers.start_conv import *

from tgbot.models import User
import logging

logger = logging.getLogger(__name__)

def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """    

    # admin commands
    dp.add_handler(CommandHandler("admin", admin.admin))
    dp.add_handler(CommandHandler("stats", admin.stats))

    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))

    dp.add_handler(MessageHandler(Filters.regex(rf'^{broadcast_command} .*'), broadcast_command_with_message))

    
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

    dp.add_handler(conv_handler)
    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()
    updater.idle()


@logger.debug
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


# Global variable - best way I found to init Telegram bot
bot = Bot(TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]