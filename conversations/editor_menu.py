from telegram.ext import MessageHandler, ConversationHandler, Filters

from all_json import CONTENT, KEYBOARDS, MESSAGES
from all_conversations import add_task_conversation, edit_delete_task_conversation

import keyboards
import tasks


# Function for exiting from conversation
def exit_from_conversation(update):
    update.message.reply_text(CONTENT["signboard"]["main_menu"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("main_menu", "ru"))

    return ConversationHandler.END


# Function - handler for editor button. Buttons: add task, edit task, back.
def handler(update, context):
    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["editor_menu"], "ru")

    if pushed_button == "add_task":
        update.message.reply_text(MESSAGES["write_task_title"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("cancel", "ru"))
        return "add_task"

    elif pushed_button == "edit_task":
        if tasks.get_user_tasks(update.message.from_user.id):
            update.message.reply_text(MESSAGES["choice_task"]["ru"],
                                      reply_markup=keyboards.get_tasks_keyboard
                                      (update.message.from_user.id, "ru"))
            return "edit_task"
        else:
            update.message.reply_text(MESSAGES["not_tasks"]["ru"])
            return "editor_menu"

    elif pushed_button == "back":
        return exit_from_conversation(update)

    else:
        update.message.reply_text(MESSAGES["click_buttons"]["ru"])
        return "editor_menu"


# Conversation schema
editor_menu_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, handler)],

    states={
        "editor_menu": [MessageHandler(Filters.text, handler)],
        "add_task": [add_task_conversation],
        "edit_task": [edit_delete_task_conversation],
    },

    fallbacks=[],
    map_to_parent={
        ConversationHandler.END: "main_menu"
    }
)
