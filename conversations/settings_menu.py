from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from all_json import SETTINGS, CONTENT, KEYBOARDS
from conversations.conversations_list import add_task_conversation, edit_task_conversation, \
    delete_task_conversation
import json

import keyboards
import weekdays
import tasks

# TODO: make settings conversation
settings_menu_conversation = ConversationHandler(
    entry_points=[],

    states={

    },

    fallbacks=[]
)
