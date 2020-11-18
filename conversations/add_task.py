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
    if keyboards.check_button(update, KEYBOARDS["static"]["cancel"], "ru") == "cancel":
        return exit_from_conversation(update)

    context.user_data["new_task"] = {}
    context.user_data["new_task"]["title"] = update.message.text

    update.message.reply_text(CONTENT["message"]["write_task_weekdays"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("cancel_back", "ru"))

    return "weekdays_handler"


def weekdays_handler(update, context):
    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["cancel_back"], "ru")

    if pushed_button == "cancel":
        return exit_from_conversation(update)

    if pushed_button == "back":
        update.message.reply_text(CONTENT["message"]["write_task_title"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("cancel", "ru"))
        return "title_handler"

    weekdays_str = weekdays.get_weekdays_from_str(update.message.text, "ru")

    if not weekdays_str:
        update.message.reply_text(CONTENT["message"]["invalid_input"]["ru"])
        return "weekdays_handler"

    context.user_data["new_task"]["weekdays"] = ''.join(weekdays_str)

    tasks.add_task(update.message.from_user.id,
                   context.user_data["new_task"]["title"],
                   context.user_data["new_task"]["weekdays"])

    context.user_data["new_task"] = {}

    update.message.reply_text(CONTENT["message"]["task_added"]["ru"])

    return exit_from_conversation(update)


add_task_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, title_handler, pass_user_data=True)],

    states={
        "title_handler": [MessageHandler(Filters.text, title_handler, pass_user_data=True)],
        "weekdays_handler": [MessageHandler(Filters.text, weekdays_handler, pass_user_data=True)]
    },

    fallbacks=[],

    map_to_parent={
        ConversationHandler.END: "editor_menu"
    }
)
