"""Module for sending menus to user"""

from keyboards import get_menu_keyboard, get_tasks_keyboard
from messages import get_signboard, get_message
from languages import get_user_language


# Function for sending main menu
def send_main_menu(update):
    # Get user language
    language = get_user_language(update=update, short=True)

    # Send menu
    update.message.reply_text(
        get_signboard("main_menu", language),
        reply_markup=get_menu_keyboard("main_menu", language)
    )


# Function for sending editor menu
def send_editor_menu(update):
    # Get user language
    language = get_user_language(update=update, short=True)

    # Send menu
    update.message.reply_text(
        get_signboard("editor_menu", language),
        reply_markup=get_menu_keyboard("editor_menu", language)
    )


# Function for sending settings menu
def send_settings_menu(update):
    # Get user language
    language = get_user_language(update=update, short=True)

    # Send menu
    update.message.reply_text(
        get_signboard("settings_menu", language),
        reply_markup=get_menu_keyboard("settings_menu", language)
    )


# Function for sending edit task menu
def send_edit_mode_menu(update):
    # Get user language
    language = get_user_language(update=update, short=True)

    # Send menu
    update.message.reply_text(
        get_message("choice_action", language),
        reply_markup=get_menu_keyboard("edit_task_menu", language)
    )


# Function for sending menu for tasks choice
def send_choice_tasks_menu(update, page=0):
    # Get user id and user language
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    # Get tasks keyboard
    keyboard = get_tasks_keyboard(user_id, language, page=page)

    # If keyboard doesn't exist - return False
    if not keyboard:
        return False

    # Send menu
    update.message.reply_text(
        get_message("choice_task", language),
        reply_markup=keyboard
    )

    # Return True, if message sent
    return True
