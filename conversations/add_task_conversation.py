from telegram.ext import MessageHandler, ConversationHandler, Filters

from all_json import KEYBOARDS, MESSAGES

from days_of_the_week import get_days_of_the_week_from_string
from keyboards import get_menu_keyboard, check_button
from tasks import get_user_tasks, add_task
from languages import get_user_language
from menu import send_editor_menu


# Function for exiting from conversation
def exit_from_conversation(update):
    send_editor_menu(update)
    return ConversationHandler.END


# Function - handler for title for a new task
def title_handler(update, context):
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    pushed_button = check_button(
        update, KEYBOARDS["static"]["cancel"], language
    )

    if pushed_button == "cancel":
        return exit_from_conversation(update)

    task_titles_list = get_user_tasks(user_id, only_titles=True)

    if update.message.text in task_titles_list:
        update.message.reply_text(MESSAGES["task_exist"][language])
        return "title_handler"

    context.user_data["new_task"] = {}
    context.user_data["new_task"]["title"] = update.message.text

    update.message.reply_text(
        MESSAGES["write_task_days_of_the_week"][language],
        reply_markup=get_menu_keyboard("cancel_back", language)
    )

    return "days_of_the_week_handler"


# Function - handler for days of the week for a new task
def days_of_the_week_handler(update, context):
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    pushed_button = check_button(
        update, KEYBOARDS["static"]["cancel_back"], language
    )

    if pushed_button == "cancel":
        return exit_from_conversation(update)

    if pushed_button == "back":
        update.message.reply_text(
            MESSAGES["write_task_title"][language],
            reply_markup=get_menu_keyboard("cancel", language)
        )

        return "title_handler"

    days_of_the_week_str = get_days_of_the_week_from_string(
        update.message.text, language
    )

    if not days_of_the_week_str:
        update.message.reply_text(MESSAGES["invalid_input"][language])
        return "days_of_the_week_handler"

    context.user_data["new_task"]["days_of_the_week"] = "".join(
        days_of_the_week_str
    )

    new_task_data = context.user_data["new_task"]

    add_task(
        user_id,
        new_task_data["title"],
        new_task_data["days_of_the_week"]
    )

    context.user_data["new_task"] = {}

    update.message.reply_text(MESSAGES["task_added"][language])

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
