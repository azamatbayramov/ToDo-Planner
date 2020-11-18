from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from data.models import Task
from data import db_session
from all_json import SETTINGS, CONTENT, KEYBOARDS
from conversations.conversations_list import main_menu_conversation
import json
import datetime
import emoji

import keyboards
import weekdays
import tasks


# Database initialization
db_session.global_init("db/database.sqlite")


def main():
    updater = Updater(SETTINGS["telegram_api_token"], use_context=True)

    dp = updater.dispatcher

    dp.add_handler(main_menu_conversation)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
