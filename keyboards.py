from data import db_session
from telegram import ReplyKeyboardMarkup
import json
from emoji import emojize

import tasks

CONTENT = json.load(open('content.json', encoding="utf8"))
KEYBOARDS = json.load(open('keyboards.json', encoding="utf8"))
SETTINGS = json.load(open('settings.json', encoding="utf8"))


def get_tasks_keyboard(user_id, language, page=0):
    tasks_list = tasks.get_user_tasks(user_id)
    tasks_list.sort(lambda task: task.title)

    if len(tasks_list) > SETTINGS["keyboard_tasks_count"]:
        tasks_list = tasks_list[SETTINGS["keyboard_tasks_count"] * page - 1:
                                SETTINGS["keyboard_tasks_count"] * (page + 1)]

    keyboard_scheme = KEYBOARDS["dynamic"]["tasks_keyboard"][f"count_{len(tasks_list)}"]
    keyboard_list = []

    task_index = 0

    def get_next_task():
        global task_index
        task = tasks_list[task_index]
        task_index += 1
        return task

    for row in keyboard_scheme:
        keyboard_list.append([])
        for button in row:
            if button == "{task}":
                keyboard_list[-1].append(get_next_task().title)
            else:
                keyboard_list[-1].append(emojize(CONTENT["button"][button]["emoji"])
                                         + CONTENT["button"][button][language])

    return ReplyKeyboardMarkup(keyboard_list, one_time_keyboard=False)


def get_menu_keyboard(keyboard, language):
    keyboard_scheme = KEYBOARDS["static"][keyboard]
    keyboard_list = []

    for row in keyboard_scheme:
        keyboard_list.append([])
        for button in row:
            keyboard_list[-1].append(emojize(CONTENT["button"][button]["emoji"])
                                     + CONTENT["button"][button][language])

    return ReplyKeyboardMarkup(keyboard_list, one_time_keyboard=False, resize_keyboard=True)


def check_button(update, keyboard, language):
    for row in KEYBOARDS["static"][keyboard]:
        for button in row:
            if update.message.text == CONTENT["button"][button][language]:
                return button

            elif update.message.text[1:] == CONTENT["button"][button][language]:
                return button

    return False
