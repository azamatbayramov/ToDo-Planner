from keyboards import get_menu_keyboard, get_tasks_keyboard
from messages import get_signboard, get_message
from languages import get_user_language


def send_main_menu(update):
    language = get_user_language(update=update, short=True)

    update.message.reply_text(
        get_signboard("main_menu", language),
        reply_markup=get_menu_keyboard("main_menu", language)
    )


def send_editor_menu(update):
    language = get_user_language(update=update, short=True)

    update.message.reply_text(
        get_signboard("editor_menu", language),
        reply_markup=get_menu_keyboard("editor_menu", language)
    )


def send_settings_menu(update):
    language = get_user_language(update=update, short=True)

    update.message.reply_text(
        get_signboard("settings_menu", language),
        reply_markup=get_menu_keyboard("settings_menu", language)
    )


def send_edit_mode_menu(update):
    language = get_user_language(update=update, short=True)

    update.message.reply_text(
        get_message("choice_action", language),
        reply_markup=get_menu_keyboard("edit_task_menu", language)
    )


def send_choice_tasks_menu(update, page=0):
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    keyboard = get_tasks_keyboard(user_id, language, page=page)

    if not keyboard:
        return False

    update.message.reply_text(
        get_message("choice_task", language),
        reply_markup=keyboard
    )

    return True
