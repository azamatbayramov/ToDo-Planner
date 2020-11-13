from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler

from data.__all_models import users, tasks
from data import db_session

import json
import datetime
import keyboards
import weekdays

# Extracting settings and content from json
SETTINGS = json.load(open("settings.json"))
CONTENT = json.load(open('content.json', encoding="utf8"))

# Extracting classes
User = users.User
Task = tasks.Task

# Database initialization
db_session.global_init("db/database.sqlite")


def send_menu(update, menu_type):
    update.message.reply_text(CONTENT["signboard"][menu_type]["ru"],
                              reply_markup=keyboards.get_keyboard(menu_type, "ru"))


def start(update, context):
    update.message.reply_text(CONTENT["message"]["welcome"]["ru"])

    send_menu(update, "main_menu")
    return 'main_menu'


def main_menu_handler(update, context):
    if update.message.text == CONTENT["button"]["today_tasks"]["ru"]:
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

    elif update.message.text == CONTENT["button"]["editor"]["ru"]:
        update.message.reply_text(CONTENT["signboard"]["editor_menu"]["ru"],
                                  reply_markup=keyboards.get_keyboard("editor_menu", "ru"))
        return "editor"


def editor_menu_handler(update, context):
    if update.message.text == CONTENT["button"]["add_task"]["ru"]:
        update.message.reply_text(CONTENT["message"]["write_task_title"]["ru"],
                                  reply_markup=keyboards.get_keyboard("cancel_keyboard", "ru"))
        return "add_task"

    elif update.message.text == CONTENT["button"]["edit_task"]["ru"]:
        # TODO: add function to edit tasks
        return "editor_menu"

    elif update.message.text == CONTENT["button"]["delete_task"]["ru"]:
        # TODO: add function to delete tasks
        return "editor_menu"

    elif update.message.text == CONTENT["button"]["back"]["ru"]:
        send_menu(update, "main_menu")
        return ConversationHandler.END


def add_task_handler_title(update, context):
    if update.message.text == CONTENT["button"]["cancel"]["ru"]:
        send_menu(update, "editor_menu")
        return ConversationHandler.END
    context.user_data["new_task"] = {}
    context.user_data["new_task"]["title"] = update.message.text

    update.message.reply_text(CONTENT["message"]["write_task_weekdays"]["ru"],
                              reply_markup=keyboards.get_keyboard("cancel_back_keyboard", "ru"))

    return "weekdays"


def add_task_handler_weekdays(update, context):
    if update.message.text == CONTENT["button"]["cancel"]["ru"]:
        send_menu(update, "editor_menu")
        return ConversationHandler.END
    if update.message.text == CONTENT["button"]["back"]["ru"]:
        update.message.reply_text(CONTENT["message"]["write_task_title"]["ru"],
                                  reply_markup=keyboards.get_keyboard("cancel_keyboard", "ru"))
        return "title"

    weekdays_str = weekdays.get_weekdays_from_str(update.message.text, "ru")

    if not weekdays_str:
        update.message.reply_text(CONTENT["message"]["invalid_input"]["ru"])
        return "weekdays"
    context.user_data["new_task"]["weekdays"] = ''.join(weekdays_str)

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
