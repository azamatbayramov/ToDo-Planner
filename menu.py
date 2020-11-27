from all_json import CONTENT

import keyboards
import languages


def send_main_menu(update):
    update.message.reply_text(
        CONTENT["signboard"]["main_menu"]["ru"],
        reply_markup=keyboards.get_menu_keyboard("main_menu", "ru")
    )


def send_editor_menu(update):
    update.message.reply_text(
        CONTENT["signboard"]["editor_menu"]["ru"],
        reply_markup=keyboards.get_menu_keyboard("editor_menu", "ru")
    )


def send_settings_menu(update):
    user_id = update.message.from_user.id
    language = languages.get_user_language(user_id)
    update.message.reply_text(
        CONTENT["signboard"]["settings_menu"][language["short"]],
        reply_markup=keyboards.get_menu_keyboard("settings_menu",
                                                 language["short"])
    )

    return "menu_handler"
