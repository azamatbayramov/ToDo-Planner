from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from all_json import SETTINGS, CONTENT, KEYBOARDS
import json

import keyboards
import weekdays
import tasks


def exit_from_conversation(update):
    update.message.reply_text(CONTENT["signboard"]["editor_menu"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("editor_menu", "ru"))

    return ConversationHandler.END


def title_handler(update, context):
    pushed_button = keyboards.check_button(update, "cancel_back_next", "ru")

    if pushed_button == "cancel":
        return exit_from_conversation(update)

    elif pushed_button == "next":
        if "page" in context:
            context["page"] += 1
        else:
            context["page"] = 1


edit_task_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, title_handler, pass_user_data=True)],

    states={

    },

    fallbacks=[],

    map_to_parent={
        ConversationHandler.END: "editor_menu"
    }
)
