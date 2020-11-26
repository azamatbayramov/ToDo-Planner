from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram.ext import Filters

from all_conversations import settings_menu_conversation
from all_conversations import editor_menu_conversation

from all_json import CONTENT, KEYBOARDS, MESSAGES

from data.models import Task
from data import db_session

import days_of_the_week
import keyboards


# Function for send user main menu's message and keyboard
def send_menu(update):
    update.message.reply_text(
        CONTENT["signboard"]["main_menu"]["ru"],
        reply_markup=keyboards.get_menu_keyboard("main_menu", "ru")
    )


# Function for send greeting and send main menu fo user
# Used for the command /start
def start_handler(update, context):
    update.message.reply_text(MESSAGES["welcome"]["ru"])
    send_menu(update)

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
        update.message.reply_text(
            CONTENT["signboard"]["editor_menu"]["ru"],
            reply_markup=keyboards.get_menu_keyboard("editor_menu", "ru")
        )

        return "editor"

    elif pushed_button == "settings":
        update.message.reply_text(
            CONTENT["signboard"]["settings_menu"]["ru"],
            reply_markup=keyboards.get_menu_keyboard("settings_menu", "ru")
        )

        return "settings"

    else:
        update.message.reply_text(MESSAGES["click_buttons"]["ru"])
        send_menu(update)

        return "main_menu"


# Conversation scheme
main_menu_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_handler),
        MessageHandler(Filters.text, handler)
    ],

    states={
        "main_menu": [MessageHandler(Filters.text, handler)],
        "editor": [editor_menu_conversation],
        "settings": [settings_menu_conversation]
    },

    fallbacks=[]
)
