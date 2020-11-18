from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from data.models import Task
from data import db_session
from all_json import SETTINGS, CONTENT, KEYBOARDS
from conversations.conversations_list import editor_menu_conversation, settings_menu_conversation
import json

import keyboards
import weekdays
import tasks


def start(update, context):
    update.message.reply_text(CONTENT["message"]["welcome"]["ru"])
    update.message.reply_text(CONTENT["signboard"]["main_menu"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("main_menu", "ru"))

    return 'main_menu'


def handler(update, context):
    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["main_menu"], "ru")

    if pushed_button == "today_tasks":
        today_weekday = weekdays.today()
        session = db_session.create_session()

        today_tasks = session.query(Task).filter(Task.user_id == update.message.from_user.id,
                                                 Task.weekdays.like(f"%{today_weekday}%")).all()

        if today_tasks:
            text = CONTENT["message"]["today_tasks"]["ru"] + '\n\n'
            for task in today_tasks:
                text += task.title + "\n"
        else:
            text = CONTENT["message"]["not_tasks_today"]["ru"]

        update.message.reply_text(text)

        session.close()

        return "main_menu"

    elif pushed_button == "editor":
        update.message.reply_text(CONTENT["signboard"]["editor_menu"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("editor_menu", "ru"))
        return "editor"


main_menu_conversation = ConversationHandler(
    entry_points=[CommandHandler("start", start)],

    states={
        "main_menu": [MessageHandler(Filters.text, handler)],
        "editor": [editor_menu_conversation],
        "settings": [settings_menu_conversation]
    },

    fallbacks=[]
)
