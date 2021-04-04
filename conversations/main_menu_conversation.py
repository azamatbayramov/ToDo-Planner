"""Module for main menu"""

from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram.ext import Filters

from conversation_handlers import settings_menu_conversation_handler
from conversation_handlers import editor_menu_conversation_handler

from menu import send_main_menu, send_editor_menu, send_settings_menu

from all_json import KEYBOARDS

from languages import get_user_language
from keyboards import check_button
from tasks import get_user_tasks
from messages import get_message


# Function for send greeting and send main menu fo user
# Used for the command /start
def start_handler(update, context):
    language = get_user_language(update=update, short=True)

    update.message.reply_text(get_message("welcome", language))
    send_main_menu(update)

    return 'main_menu'


# Function - handler for main menu buttons. Buttons:
# today's tasks, editor, settings
def handler(update, context):
    # Get user id and user language
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    # Check pushed button of keyboard
    pushed_button = check_button(
        update, KEYBOARDS["static"]["main_menu"], language
    )

    # If pushed button is "today_tasks"
    if pushed_button == "today_tasks":
        # Get user's today tasks
        today_tasks = get_user_tasks(user_id, only_titles=True,
                                     today_tasks=True)

        # If user has today tasks, make list of tasks
        if today_tasks:
            text = get_message("today_tasks", language) + '\n\n'
            for task in today_tasks:
                text += task + "\n"

        # If user hasn't today tasks, say user about it
        else:
            text = get_message("not_tasks_today", language)

        update.message.reply_text(text)

        return "main_menu"

    # If pushed button is "editor", proceed to editor menu
    elif pushed_button == "editor":
        send_editor_menu(update)
        return "editor"

    # If pushed button is "settings", proceed to settings menu
    elif pushed_button == "settings":
        send_settings_menu(update)
        return "settings"

    # If user message isn't button, ask user click on the buttons
    else:
        update.message.reply_text(get_message("click_buttons", language))
        send_main_menu(update)
        return "main_menu"


# Conversation scheme
main_menu_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_handler),
        MessageHandler(Filters.text, handler)
    ],

    states={
        "main_menu": [MessageHandler(Filters.text, handler)],
        "editor": [editor_menu_conversation_handler],
        "settings": [settings_menu_conversation_handler]
    },

    fallbacks=[]
)
