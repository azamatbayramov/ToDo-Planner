from telegram.ext import MessageHandler, ConversationHandler, Filters
from all_conversations import edit_delete_task_conversation
from all_conversations import add_task_conversation
from all_json import CONTENT, KEYBOARDS, MESSAGES
import keyboards
import tasks


# Function for send user editor menu's message and keyboard
def send_menu(update):
    update.message.reply_text(
        CONTENT["signboard"]["editor_menu"]["ru"],
        reply_markup=keyboards.get_menu_keyboard("editor_menu", "ru")
    )


# Function for exiting from conversation
def exit_from_conversation(update):
    update.message.reply_text(
        CONTENT["signboard"]["main_menu"]["ru"],
        reply_markup=keyboards.get_menu_keyboard("main_menu", "ru")
    )

    return ConversationHandler.END


# Function - handler for editor button. Buttons: add task, edit task, back.
def handler(update, context):
    user_id = update.message.from_user.id
    pushed_button = keyboards.check_button(update,
                                           KEYBOARDS["static"]["editor_menu"],
                                           "ru")

    if pushed_button == "add_task":
        update.message.reply_text(
            MESSAGES["write_task_title"]["ru"],
            reply_markup=keyboards.get_menu_keyboard("cancel", "ru")
        )

        return "add_task"

    elif pushed_button == "edit_task":
        if tasks.get_user_tasks(user_id):
            update.message.reply_text(
                MESSAGES["choice_task"]["ru"],
                reply_markup=keyboards.get_tasks_keyboard(user_id, "ru")
            )

            return "edit_task"
        else:
            update.message.reply_text(MESSAGES["not_tasks"]["ru"])
            send_menu(update)
            return "editor_menu"

    elif pushed_button == "back":
        return exit_from_conversation(update)

    else:
        update.message.reply_text(MESSAGES["click_buttons"]["ru"])
        send_menu(update)

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
