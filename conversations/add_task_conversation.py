"""Module for task adding conversation"""

from telegram.ext import MessageHandler, ConversationHandler, Filters

from all_json import KEYBOARDS

from days_of_the_week import get_days_of_the_week_from_string
from keyboards import get_menu_keyboard, check_button
from tasks import get_user_tasks, add_task
from languages import get_user_language
from menu import send_editor_menu
from messages import get_message


# Function for exiting from conversation
def exit_from_conversation(update):
    send_editor_menu(update)
    return ConversationHandler.END


# Function - handler for title for a new task
def title_handler(update, context):
    # Get user id and user language
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    # Check pushed button of keyboard
    pushed_button = check_button(
        update, KEYBOARDS["static"]["cancel"], language
    )

    # If pushed button is "cancel" exit user from conversation
    if pushed_button == "cancel":
        return exit_from_conversation(update)

    # Check if user have task with such title
    if update.message.text in get_user_tasks(user_id, only_titles=True):
        update.message.reply_text(get_message("task_exist", language))
        return "title_handler"

    # Clear context.user_data for new task and load title there
    context.user_data["new_task"] = {}
    context.user_data["new_task"]["title"] = update.message.text

    # Send message to write days of the week of the task
    update.message.reply_text(
        get_message("write_task_days_of_the_week", language),
        reply_markup=get_menu_keyboard("cancel_back", language)
    )

    return "days_of_the_week_handler"


# Function - handler for days of the week for a new task
def days_of_the_week_handler(update, context):
    # Get user id and user language
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    # Check pushed button of keyboard
    pushed_button = check_button(
        update, KEYBOARDS["static"]["cancel_back"], language
    )

    # If pushed button is "cancel" exit user from conversation
    if pushed_button == "cancel":
        return exit_from_conversation(update)

    # If pushed button is "back" return user to previous
    # stage of task adding - write task title
    if pushed_button == "back":
        update.message.reply_text(
            get_message("write_task_title", language),
            reply_markup=get_menu_keyboard("cancel", language)
        )

        return "title_handler"

    # Get days of the week from user message
    days_of_the_week_str = get_days_of_the_week_from_string(
        update.message.text, language
    )

    # Check if message is incorrect
    if not days_of_the_week_str:
        update.message.reply_text(get_message("invalid_input", language))
        return "days_of_the_week_handler"

    # Load days of the week to context.user_data for new task
    context.user_data["new_task"]["days_of_the_week"] = days_of_the_week_str

    # Get data from context.user_data
    new_task_data = context.user_data["new_task"]

    # Add new task to database
    add_task(
        user_id,
        new_task_data["title"],
        new_task_data["days_of_the_week"]
    )

    # Clear context.user_data for new task
    context.user_data["new_task"] = {}

    # Send message to user about successful adding
    update.message.reply_text(get_message("task_added", language))

    # Exit from conversation
    return exit_from_conversation(update)


# Conversation scheme
add_task_conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.text, title_handler, pass_user_data=True)
    ],

    states={
        "title_handler": [
            MessageHandler(Filters.text, title_handler, pass_user_data=True)
        ],
        "days_of_the_week_handler": [
            MessageHandler(
                Filters.text, days_of_the_week_handler, pass_user_data=True
            )
        ]
    },

    fallbacks=[],

    map_to_parent={
        ConversationHandler.END: "editor_menu"
    }
)
