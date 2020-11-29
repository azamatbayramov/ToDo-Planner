from telegram.ext import MessageHandler, ConversationHandler, Filters
from all_json import KEYBOARDS, MESSAGES, LANGUAGES
from data import db_session
from menu import send_main_menu, send_settings_menu
from data.models import User
import languages
import keyboards


# Function for exiting from conversation
def exit_from_conversation(update):
    send_main_menu(update)
    return ConversationHandler.END


# Function - handler for settings menu button
def menu_handler(update, context):
    language = languages.get_user_language(update=update, short=True)

    pushed_button = keyboards.check_button(
        update, KEYBOARDS["static"]["settings_menu"], language
    )

    if pushed_button == "back":
        return exit_from_conversation(update)

    elif pushed_button == "choice_language":
        update.message.reply_text(
            MESSAGES["choice_language"][language],
            reply_markup=keyboards.get_languages_menu(language)
        )

        return "language_handler"


# Function - handler for language for editing a user language
def language_handler(update, context):
    user_id = update.message.from_user.id
    user_language = languages.get_user_language(user_id=user_id, short=True)

    text = update.message.text

    selected_language = {}

    pushed_button = keyboards.check_button(
        update, [["back"]], user_language
    )

    if pushed_button == "back":
        send_settings_menu(update)
        return "menu_handler"

    for language in LANGUAGES:
        if language["title"].lower() in text.lower():
            selected_language = language
            break

    if selected_language:
        session = db_session.create_session()
        user = session.query(User).filter(User.telegram_id == user_id).first()
        user.language_id = selected_language["id"]
        session.commit()
        session.close()

        update.message.reply_text(
            MESSAGES["language_changed"][selected_language["short"]]
        )

        send_settings_menu(update)
        return "menu_handler"
    else:
        update.message.reply_text(MESSAGES["click_buttons"][user_language])
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
