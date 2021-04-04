from telegram.ext import MessageHandler, ConversationHandler, Filters

from all_json import KEYBOARDS, LANGUAGES

from data import db_session
from data.models import User

from keyboards import check_button, get_languages_menu
from menu import send_main_menu, send_settings_menu
from languages import get_user_language
from messages import get_message


# Function for exiting from conversation
def exit_from_conversation(update):
    send_main_menu(update)
    return ConversationHandler.END


# Function - handler for settings menu button
def menu_handler(update, context):
    # Get user language
    language = get_user_language(update=update, short=True)

    # Check pushed button of keyboard
    pushed_button = check_button(
        update, KEYBOARDS["static"]["settings_menu"], language
    )

    # If pushed button is "back", exit from conversation
    if pushed_button == "back":
        return exit_from_conversation(update)

    # If pushed button is "choice_language", proceed to choice language menu
    elif pushed_button == "choice_language":
        update.message.reply_text(
            get_message("choice_language", language),
            reply_markup=get_languages_menu(language)
        )

        return "language_handler"


# Function - handler for language for editing a user language
def language_handler(update, context):
    # Get user id and user language
    user_id = update.message.from_user.id
    user_language = get_user_language(user_id=user_id, short=True)

    # Check pushed button of keyboard
    pushed_button = check_button(
        update, [["back"]], user_language
    )

    # If pushed button is "back", return to settings menu
    if pushed_button == "back":
        send_settings_menu(update)
        return "menu_handler"

    # Get user message
    text = update.message.text

    selected_language = {}

    # Check if user message is language
    for language in LANGUAGES:
        if language["title"].lower() in text.lower():
            selected_language = language
            break

    # If user message is language
    if selected_language:
        # Create database session
        session = db_session.create_session()

        # Edit user's language in database
        user = session.query(User).filter(User.telegram_id == user_id).first()
        user.language_id = selected_language["id"]

        # Commit and close database session
        session.commit()
        session.close()

        # Say user that language changed
        update.message.reply_text(
            get_message(
                "language_changed",
                selected_language["short"],
                selected_language["emoji"]
            )
        )

        # Return to settings menu
        send_settings_menu(update)
        return "menu_handler"

    # If user message isn't button, ask user click on the buttons
    else:
        update.message.reply_text(get_message("click_buttons", user_language))
        return "language_handler"


# Conversation scheme
settings_menu_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, menu_handler)],

    states={
        "menu_handler": [MessageHandler(Filters.text, menu_handler)],
        "language_handler": [MessageHandler(Filters.text, language_handler)]
    },

    fallbacks=[],

    map_to_parent={
        ConversationHandler.END: "main_menu"
    }
)
