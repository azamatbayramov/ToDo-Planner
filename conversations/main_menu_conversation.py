from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram.ext import Filters

from conversation_handlers import settings_menu_conversation_handler
from conversation_handlers import editor_menu_conversation_handler

from menu import send_main_menu, send_editor_menu, send_settings_menu

from all_json import KEYBOARDS, MESSAGES

from data.models import Task
from data import db_session

import days_of_the_week
import keyboards


# Function for send greeting and send main menu fo user
# Used for the command /start
def start_handler(update, context):
    update.message.reply_text(MESSAGES["welcome"]["ru"])
    send_main_menu(update)

    return 'main_menu'


# Function - handler for main menu buttons. Buttons:
# today's tasks, editor, settings
def handler(update, context):
    pushed_button = keyboards.check_button(update,
                                           KEYBOARDS["static"]["main_menu"],
                                           "ru")

    if pushed_button == "today_tasks":
        today_day_of_the_week = days_of_the_week.today_day_of_the_week()
        session = db_session.create_session()

        today_tasks = session.query(Task).filter(
            Task.user_id == update.message.from_user.id,
            Task.days_of_the_week.like(f"%{today_day_of_the_week}%")
        ).all()

        if today_tasks:
            text = MESSAGES["today_tasks"]["ru"] + '\n\n'
            for task in today_tasks:
                text += task.title + "\n"
        else:
            text = MESSAGES["not_tasks_today"]["ru"]

        update.message.reply_text(text)

        session.close()

        return "main_menu"

    elif pushed_button == "editor":
        send_editor_menu(update)
        return "editor"

    elif pushed_button == "settings":
        send_settings_menu(update)
        return "settings"

    else:
        update.message.reply_text(MESSAGES["click_buttons"]["ru"])
        send_main_menu(update)

        return "main_menu"


# Conversation scheme
main_menu_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_handler),
        MessageHandler(Filters.text, handler)
    ],

    states={
        "main_menu": [MessageHandler(Filters.text, handler)],
        "editor": [editor_menu_conversation_handler],
        "settings": [settings_menu_conversation_handler]
    },

    fallbacks=[]
)
