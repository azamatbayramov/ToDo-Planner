from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler


from data.models import Task
from data import db_session

import json
import datetime
import emoji

import keyboards
import weekdays
import tasks

# Extracting settings and content from json
SETTINGS = json.load(open("settings.json"))
CONTENT = json.load(open('content.json', encoding="utf8"))

# Database initialization
db_session.global_init("db/database.sqlite")


def send_menu(update, menu_type):
    update.message.reply_text(CONTENT["signboard"][menu_type]["ru"],
                              reply_markup=keyboards.get_menu_keyboard(menu_type, "ru"))


def start(update, context):
    update.message.reply_text(CONTENT["message"]["welcome"]["ru"])

    send_menu(update, "main_menu")
    return 'main_menu'


def main_menu_handler(update, context):
    pushed_button = keyboards.check_button(update, "main_menu", "ru")

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


def editor_menu_handler(update, context):
    pushed_button = keyboards.check_button(update, "editor_menu", "ru")

    if pushed_button == "add_task":
        update.message.reply_text(CONTENT["message"]["write_task_title"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("cancel", "ru"))
        return "add_task"

    elif pushed_button == "edit_task":
        return "editor_menu"

    elif pushed_button == "delete_task":
        # TODO: add function to delete tasks
        return "editor_menu"

    elif pushed_button == "back":
        send_menu(update, "main_menu")
        return ConversationHandler.END

    else:
        update.message.reply_text(CONTENT["message"]["click_buttons"]["ru"])
        return "editor_menu"


def add_task_handler_title(update, context):
    if keyboards.check_button(update, "cancel", "ru") == "cancel":
        send_menu(update, "editor_menu")
        return ConversationHandler.END

    context.user_data["new_task"] = {}
    context.user_data["new_task"]["title"] = update.message.text

    update.message.reply_text(CONTENT["message"]["write_task_weekdays"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("cancel_back", "ru"))

    return "weekdays"


def add_task_handler_weekdays(update, context):
    pushed_button = keyboards.check_button(update, "cancel_back", "ru")

    if pushed_button == "cancel":
        send_menu(update, "editor_menu")
        return ConversationHandler.END

    if pushed_button == "back":
        update.message.reply_text(CONTENT["message"]["write_task_title"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("cancel", "ru"))
        return "title"

    weekdays_str = weekdays.get_weekdays_from_str(update.message.text, "ru")

    if not weekdays_str:
        update.message.reply_text(CONTENT["message"]["invalid_input"]["ru"])
        return "weekdays"

    context.user_data["new_task"]["weekdays"] = ''.join(weekdays_str)

    tasks.add_task(update.message.from_user.id,
                   context.user_data["new_task"]["title"],
                   context.user_data["new_task"]["weekdays"])

    context.user_data["new_task"] = {}

    update.message.reply_text(CONTENT["message"]["task_added"]["ru"])
    send_menu(update, "editor_menu")

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
