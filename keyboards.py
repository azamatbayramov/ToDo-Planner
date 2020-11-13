from telegram import ReplyKeyboardMarkup
import json

CONTENT = json.load(open('content.json', encoding="utf8"))
KEYBOARDS = json.load(open('keyboards.json', encoding="utf8"))


def get_keyboard(keyboard, language):
    keyboard_scheme = KEYBOARDS[keyboard]
    keyboard_list = []

    for row in keyboard_scheme:
        keyboard_list.append([])
        for button in row:
            keyboard_list[-1].append(CONTENT["button"][button][language])

    return ReplyKeyboardMarkup(keyboard_list, one_time_keyboard=False)
