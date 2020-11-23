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


# TODO: make settings conversation
settings_menu_conversation = ConversationHandler(
    entry_points=[],

    states={

    },

    fallbacks=[],

    map_to_parent={
        ConversationHandler.END: "main_menu"
    }
)
