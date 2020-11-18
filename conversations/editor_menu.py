from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from all_json import SETTINGS, CONTENT, KEYBOARDS
from conversations.conversations_list import add_task_conversation, edit_task_conversation, \
    delete_task_conversation
import json

import keyboards
import weekdays
import tasks


def exit_from_conversation(update):
    update.message.reply_text(CONTENT["signboard"]["main_menu"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("main_menu", "ru"))

    return ConversationHandler.END


def handler(update, context):
    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["editor_menu"], "ru")

    if pushed_button == "add_task":
        update.message.reply_text(CONTENT["message"]["write_task_title"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("cancel", "ru"))
        return "add_task"

    elif pushed_button == "edit_task":
        update.message.reply_text(CONTENT["message"]["choice_task"]["ru"],
                                  reply_markup=keyboards.get_tasks_keyboard
                                  (update.message.from_user.id, "ru"))
        return "edit_task"

    elif pushed_button == "delete_task":
        # TODO: add function to delete tasks
        return "editor_menu"

    elif pushed_button == "back":
        return exit_from_conversation(update)

    else:
        update.message.reply_text(CONTENT["message"]["click_buttons"]["ru"])
        return "editor_menu"


editor_menu_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, handler)],

    states={
        "editor_menu": [MessageHandler(Filters.text, handler)],
        "add_task": [add_task_conversation],
        "edit_task": [edit_task_conversation],
        "delete_task": [delete_task_conversation]
    },

    fallbacks=[],
    map_to_parent={
        ConversationHandler.END: "main_menu"
    }
)
