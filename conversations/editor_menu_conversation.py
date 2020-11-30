from telegram.ext import MessageHandler, ConversationHandler, Filters

from conversation_handlers import edit_delete_task_conversation_handler
from conversation_handlers import add_task_conversation_handler

from all_json import KEYBOARDS, MESSAGES

from menu import send_main_menu, send_editor_menu, send_choice_tasks_menu
from keyboards import check_button, get_menu_keyboard
from languages import get_user_language
from tasks import get_user_tasks


# Function for exiting from conversation
def exit_from_conversation(update):
    send_main_menu(update)
    return ConversationHandler.END


# Function - handler for editor button. Buttons: add task, edit task, back.
def handler(update, context):
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    pushed_button = check_button(
        update, KEYBOARDS["static"]["editor_menu"], language
    )

    if pushed_button == "add_task":
        update.message.reply_text(
            MESSAGES["write_task_title"][language],
            reply_markup=get_menu_keyboard("cancel", language)
        )

        return "add_task"

    elif pushed_button == "edit_task":
        if get_user_tasks(user_id):
            send_choice_tasks_menu(update)

            return "edit_task"

        else:
            update.message.reply_text(MESSAGES["not_tasks"][language])
            send_editor_menu(update)

            return "editor_menu"

    elif pushed_button == "back":
        return exit_from_conversation(update)

    else:
        update.message.reply_text(MESSAGES["click_buttons"][language])
        send_editor_menu(update)

        return "editor_menu"


# Conversation scheme
editor_menu_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, handler)],

    states={
        "editor_menu": [MessageHandler(Filters.text, handler)],
        "add_task": [add_task_conversation_handler],
        "edit_task": [edit_delete_task_conversation_handler],
    },

    fallbacks=[],

    map_to_parent={
        ConversationHandler.END: "main_menu"
    }
)
