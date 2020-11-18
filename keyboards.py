from data import db_session
from telegram import ReplyKeyboardMarkup
import json
from emoji import emojize
import math
from all_json import SETTINGS, CONTENT, KEYBOARDS
import tasks


def get_tasks_keyboard(user_id, language, page=0):
    tasks_list = tasks.get_user_tasks(user_id)
    tasks_count = len(tasks_list)
    pages_count = math.ceil(tasks_count / SETTINGS["keyboard_tasks_count"])
    last_page = pages_count - 1

    tasks_titles_list = [task.title for task in tasks_list]

    tasks_titles_list.sort()

    if tasks_count > SETTINGS["keyboard_tasks_count"]:
        start_index = SETTINGS["keyboard_tasks_count"] * page
        finish_index = SETTINGS["keyboard_tasks_count"] * (page + 1)

        if finish_index > len(tasks_titles_list):
            tasks_titles_list = tasks_titles_list[start_index:]
        else:
            tasks_titles_list = tasks_titles_list[start_index:finish_index]

    keyboard_scheme = KEYBOARDS["dynamic"]["tasks_keyboard"][f"count_{len(tasks_titles_list)}"]
    keyboard_list = []

    task_index = 0

    def get_next_task_title():
        nonlocal task_index
        task_title = tasks_titles_list[task_index]
        task_index += 1
        return task_title

    for row in keyboard_scheme:
        keyboard_list.append([])
        for button in row:
            if button == "{task}":
                keyboard_list[-1].append(get_next_task_title())
            else:
                if button == "back" and (pages_count == 1 or page == 0):
                    continue
                if button == "next" and (pages_count == 1 or page == last_page):
                    continue
                print(button)
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


def check_button(update, keyboard_list, language):
    for row in keyboard_list:
        for button in row:
            if update.message.text == CONTENT["button"][button][language]:
                return button

            elif update.message.text[1:] == CONTENT["button"][button][language]:
                return button

    return False