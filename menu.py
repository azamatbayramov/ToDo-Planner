from all_json import CONTENT

import keyboards
import languages


def send_main_menu(update):
    language = languages.get_user_language(update=update, short=True)

    update.message.reply_text(
        CONTENT["signboard"]["main_menu"][language],
        reply_markup=keyboards.get_menu_keyboard("main_menu", language)
    )


def send_editor_menu(update):
    language = languages.get_user_language(update=update, short=True)

    update.message.reply_text(
        CONTENT["signboard"]["editor_menu"][language],
        reply_markup=keyboards.get_menu_keyboard("editor_menu", language)
    )


def send_settings_menu(update):
    language = languages.get_user_language(update=update, short=True)

    update.message.reply_text(
        CONTENT["signboard"]["settings_menu"][language],
        reply_markup=keyboards.get_menu_keyboard("settings_menu", language)
    )

    return "menu_handler"
