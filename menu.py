from all_json import SIGNBOARDS

import keyboards
import languages


def send_main_menu(update):
    language = languages.get_user_language(update=update, short=True)

    update.message.reply_text(
        SIGNBOARDS["main_menu"][language],
        reply_markup=keyboards.get_menu_keyboard("main_menu", language)
    )


def send_editor_menu(update):
    language = languages.get_user_language(update=update, short=True)

    update.message.reply_text(
        SIGNBOARDS["editor_menu"][language],
        reply_markup=keyboards.get_menu_keyboard("editor_menu", language)
    )


def send_settings_menu(update):
    language = languages.get_user_language(update=update, short=True)

    update.message.reply_text(
        SIGNBOARDS["settings_menu"][language],
        reply_markup=keyboards.get_menu_keyboard("settings_menu", language)
    )

    return "menu_handler"
