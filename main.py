from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler

from data.__all_models import users, tasks
from data import db_session

import json
import datetime

# Extracting settings and content from json
SETTINGS = json.load(open("settings.json"))
CONTENT = json.load(open('content.json', encoding="utf8"))

# Extracting classes
User = users.User
Task = tasks.Task

# Database initialization
db_session.global_init("db/database.sqlite")


def start(update, context):
    update.message.reply_text(CONTENT["message"]["welcome"]["ru"])
    return 'main_menu'


def get_today_weekday():
    return datetime.datetime.today().weekday() + 1


def main_menu_handler(update, context):
    if update.message.text == CONTENT["button"]["today_tasks"]["ru"]:
        today_weekday = get_today_weekday()
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

    elif update.message.text == CONTENT["button"]["editor"]["ru"]:
        update.message.reply_text(CONTENT["signboard"]["editor_menu"]["ru"])
        return "editor"


def editor_menu_handler(update, context):
    print(update.message.text)
    print(CONTENT["button"]["back"]["ru"])
    print(update.message.text == CONTENT["button"]["back"]["ru"])

    if update.message.text == CONTENT["button"]["add_task"]["ru"]:
        update.message.reply_text(CONTENT["message"]["write_task_title"]["ru"])
        return "add_task"

    elif update.message.text == CONTENT["button"]["edit_task"]["ru"]:
        # TODO: add function to edit tasks
        return "editor_menu"

    elif update.message.text == CONTENT["button"]["delete_task"]["ru"]:
        # TODO: add function to delete tasks
        return "editor_menu"

    elif update.message.text == CONTENT["button"]["back"]["ru"]:
        update.message.reply_text(CONTENT["signboard"]["main_menu"]["ru"])
        return ConversationHandler.END


def add_task_handler_title(update, context):
    context.user_data["new_task"] = {}
    context.user_data["new_task"]["title"] = update.message.text
    update.message.reply_text(CONTENT["message"]["write_task_weekdays"]["ru"])
    return "weekdays"


def add_task_handler_weekdays(update, context):
    weekdays = update.message.text.split()
    weekdays.sort()
    context.user_data["new_task"]["weekdays"] = ''.join(weekdays)

    new_task = Task()
    new_task.user_id = update.message.from_user.id
    new_task.title = context.user_data["new_task"]["title"]
    new_task.weekdays = context.user_data["new_task"]["weekdays"]

    session = db_session.create_session()
    session.add(new_task)
    session.commit()
    session.close()

    context.user_data["new_task"] = {}

    update.message.reply_text(CONTENT["message"]["task_added"]["ru"])

    return ConversationHandler.END


add_task_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, add_task_handler_title, pass_user_data=True)],

    states={
        "title": [MessageHandler(Filters.text, add_task_handler_title, pass_user_data=True)],
        "weekdays": [MessageHandler(Filters.text, add_task_handler_weekdays, pass_user_data=True)]
    },

    fallbacks=[],
    map_to_parent={
        ConversationHandler.END: "editor_menu"
    }
)

# TODO: make edit task conversation
edit_task_conv = ConversationHandler(
    entry_points=[],

    states={

    },

    fallbacks=[]
)

# TODO: make delete task conversation
delete_task_conv = ConversationHandler(
    entry_points=[],

    states={

    },

    fallbacks=[]
)

editor_menu_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, editor_menu_handler)],

    states={
        "editor_menu": [MessageHandler(Filters.text, editor_menu_handler)],
        "add_task": [add_task_conv],
        "edit_task": [edit_task_conv],
        "delete_task": [delete_task_conv]
    },

    fallbacks=[],
    map_to_parent={
        ConversationHandler.END: "main_menu"
    }
)

# TODO: make settings conversation
settings_menu_conv = ConversationHandler(
    entry_points=[],

    states={

    },

    fallbacks=[]
)

main_menu_conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],

    states={
        "main_menu": [MessageHandler(Filters.text, main_menu_handler)],
        "editor": [editor_menu_conv],
        "settings": [settings_menu_conv]
    },

    fallbacks=[]
)


def main():
    updater = Updater(SETTINGS["telegram_api_token"], use_context=True)

    dp = updater.dispatcher

    dp.add_handler(main_menu_conv)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
