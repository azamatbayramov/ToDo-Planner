"""Module for working with keyboards"""

from telegram import ReplyKeyboardMarkup

from all_json import SETTINGS, KEYBOARDS, BUTTONS, LANGUAGES

from emoji import emojize
import math

from tasks import get_user_tasks


# Function for getting tasks keyboard
def get_tasks_keyboard(user_id, language, page=0):
    # Get user tasks(titles of task)
    tasks_titles_list = get_user_tasks(user_id, only_titles=True)

    # Get definite tasks for definite page

    tasks_count = len(tasks_titles_list)
    pages_count = math.ceil(tasks_count / SETTINGS["keyboard_tasks_count"])

    last_page = pages_count - 1

    # If page is incorrect, return False
    if page >= pages_count:
        return False

    # If tasks more, than should be in one page, separate tasks for page
    if tasks_count > SETTINGS["keyboard_tasks_count"]:
        start_index = SETTINGS["keyboard_tasks_count"] * page
        finish_index = SETTINGS["keyboard_tasks_count"] * (page + 1)

        if finish_index > len(tasks_titles_list):
            tasks_titles_list = tasks_titles_list[start_index:]
        else:
            tasks_titles_list = tasks_titles_list[start_index:finish_index]

    # Get keyboard scheme
    keyboard_scheme = KEYBOARDS["dynamic"]["tasks_keyboard"][
        f"count_{len(tasks_titles_list)}"
    ]

    keyboard_list = []

    task_index = 0

    # Internal function for getting next task to fill keyboard list
    def get_next_task_title():
        nonlocal task_index
        task_title = tasks_titles_list[task_index]
        task_index += 1
        return task_title

    # Fill keyboard list according to the scheme
    for row in keyboard_scheme:
        keyboard_list.append([])

        for button in row:
            if button == "{task}":
                keyboard_list[-1].append(get_next_task_title())
            else:
                if button == "back" and (pages_count == 1 or page == 0):
                    continue
                if button == "next" and (pages_count == 1 or
                                         page == last_page):
                    continue

                keyboard_list[-1].append(
                    emojize(BUTTONS[button]["emoji"], use_aliases=True)
                    + BUTTONS[button][language]
                )

    # Return keyboard from keyboard list
    return ReplyKeyboardMarkup(
        keyboard_list, one_time_keyboard=False, resize_keyboard=True
    )


# Function for getting menu keyboard
def get_menu_keyboard(keyboard, language):
    # Get keyboard scheme
    keyboard_scheme = KEYBOARDS["static"][keyboard]
    keyboard_list = []

    # Fill keyboard list according to the scheme
    for row in keyboard_scheme:
        keyboard_list.append([])

        for button in row:
            keyboard_list[-1].append(
                emojize(BUTTONS[button]["emoji"], use_aliases=True)
                + BUTTONS[button][language]
            )

    # Return keyboard from keyboard list
    return ReplyKeyboardMarkup(
        keyboard_list, one_time_keyboard=False, resize_keyboard=True
    )


def get_languages_menu(user_language):
    # Get languages list
    languages_list = LANGUAGES
    keyboard_list = [[]]

    # Fill keyboard list according to the scheme
    for language in languages_list:
        if len(keyboard_list[-1]) > 3:
            keyboard_list.append([])

        keyboard_list[-1].append(
            emojize(language["emoji"], use_aliases=True) + language["title"]
        )

    keyboard_list.append(
        [emojize(BUTTONS['back']["emoji"], use_aliases=True) +
         BUTTONS['back'][user_language]]
    )

    # Return keyboard from keyboard list
    return ReplyKeyboardMarkup(
        keyboard_list, one_time_keyboard=False, resize_keyboard=True
    )


# Function for check if user message is clicked button of keyboard
def check_button(update, keyboard_list, language):
    for row in keyboard_list:
        for button in row:
            if update.message.text == BUTTONS[button][language]:
                return button

            elif update.message.text[1:] == BUTTONS[button][language]:
                return button

    return False
