from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters
from data.models import Task
from data import db_session
from all_json import CONTENT, KEYBOARDS, MESSAGES
from all_conversations import editor_menu_conversation, settings_menu_conversation
import keyboards
import days_of_the_week


def start(update, context):
    update.message.reply_text(MESSAGES["welcome"]["ru"])
    update.message.reply_text(CONTENT["signboard"]["main_menu"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("main_menu", "ru"))

    return 'main_menu'


# Function - handler for main menu buttons. Buttons: today's tasks, editor, settings(in future :D)
def handler(update, context):
    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["main_menu"], "ru")

    if pushed_button == "today_tasks":
        today_days_of_the_week = days_of_the_week.today_day_of_the_week()
        session = db_session.create_session()

        today_tasks = session.query(Task).filter(Task.user_id == update.message.from_user.id,
                                                 Task.days_of_the_week.like(
                                                     f"%{today_days_of_the_week}%")).all()

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
        update.message.reply_text(CONTENT["signboard"]["editor_menu"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("editor_menu", "ru"))
        return "editor"

    elif pushed_button == "settings":
        update.message.reply_text(CONTENT["signboard"]["settings_menu"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("settings_menu", "ru"))
        return "settings"

# Conversation schema
main_menu_conversation = ConversationHandler(
    entry_points=[CommandHandler("start", start)],

    states={
        "main_menu": [MessageHandler(Filters.text, handler)],
        "editor": [editor_menu_conversation],
        "settings": [settings_menu_conversation]
    },

    fallbacks=[]
)
