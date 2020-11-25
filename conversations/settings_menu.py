from telegram.ext import MessageHandler, ConversationHandler, Filters
from data import db_session
from all_json import CONTENT, KEYBOARDS, MESSAGES, LANGUAGES
from all_conversations import add_task_conversation, edit_delete_task_conversation
from data.models import User
import languages
import keyboards
import tasks


# Function for exiting from conversation
def exit_from_conversation(update):
    update.message.reply_text(CONTENT["signboard"]["main_menu"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("main_menu", "ru"))

    return ConversationHandler.END


def send_settings_menu(update):
    user_id = update.message.from_user.id
    language = languages.get_user_language(user_id)
    update.message.reply_text(
        CONTENT["signboard"]["settings_menu"][language["short"]],
        reply_markup=keyboards.get_menu_keyboard("settings_menu", language["short"])
    )

    return "menu_handler"


def menu_handler(update, context):
    user_id = update.message.from_user.id
    language = languages.get_user_language(user_id)
    pushed_button = keyboards.check_button(update,
                                           KEYBOARDS["static"]["settings_menu"],
                                           language["short"])
    if pushed_button == "back":
        return exit_from_conversation(update)

    elif pushed_button == "choice_language":
        update.message.reply_text(MESSAGES["choice_language"][language["short"]],
                                  reply_markup=keyboards.get_languages_menu(language["short"]))

        return "language_handler"


def language_handler(update, context):
    user_id = update.message.from_user.id
    text = update.message.text
    language = languages.get_user_language(user_id)
    selected_language = {}
    pushed_button = keyboards.check_button(update, [["back"]], language["short"])

    if pushed_button == "back":
        return send_settings_menu(update)

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

        update.message.reply_text(MESSAGES["language_changed"][selected_language["short"]])

        return send_settings_menu(update)
    else:
        update.message.reply_text(MESSAGES["click_buttons"][language["short"]])
        return "language_handler"


# TODO: make settings conversation
settings_menu_conversation = ConversationHandler(
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
