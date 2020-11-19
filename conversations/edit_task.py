from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from all_json import SETTINGS, CONTENT, KEYBOARDS
import json
from data.models import Task
from data import db_session
import keyboards
import weekdays
import tasks


def send_edit_mode_menu(update):
    update.message.reply_text(CONTENT["message"]["choice_action"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("edit_task_menu", "ru"))


def exit_from_conversation(update):
    update.message.reply_text(CONTENT["signboard"]["editor_menu"]["ru"],
                              reply_markup=keyboards.get_menu_keyboard("editor_menu", "ru"))

    return ConversationHandler.END


def choice_task_handler(update, context):
    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["cancel_back_next"], "ru")

    task_titles_list = tasks.get_user_tasks(update.message.from_user.id, only_titles=True)

    if update.message.text in task_titles_list:
        context.user_data["selected_task_id"] = tasks.get_task_id_from_title(update.message.text)

        send_edit_mode_menu(update)

        return "edit_mode_handler"

    if pushed_button == "cancel":
        return exit_from_conversation(update)

    elif pushed_button == "next":
        if "page" in context.user_data:
            context.user_data["page"] += 1
        else:
            context.user_data["page"] = 1

        keyboard = keyboards.get_tasks_keyboard(update.message.from_user.id, "ru",
                                                page=context.user_data["page"])

        if keyboard:
            update.message.reply_text(CONTENT["message"]["choice_task"]["ru"],
                                      reply_markup=keyboard)

            return "choice_task_handler"
        else:
            update.message.reply_text(CONTENT["message"]["click_buttons"]["ru"])
            context.user_data["page"] -= 1
            return "choice_task_handler"

    elif pushed_button == "back":
        if "page" in context.user_data:
            if context.user_data["page"] > 0:
                context.user_data["page"] -= 1
                update.message.reply_text(CONTENT["message"]["choice_task"]["ru"],
                                          reply_markup=keyboards.get_tasks_keyboard
                                          (update.message.from_user.id, "ru",
                                           page=context.user_data["page"]))

                return "choice_task_handler"

        update.message.reply_text(CONTENT["message"]["click_buttons"]["ru"])
        return "choice_task_handler"


def new_title_handler(update, context):
    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["cancel"], "ru")

    print(pushed_button)

    if pushed_button == "cancel":
        send_edit_mode_menu(update)

        return "edit_mode_handler"

    session = db_session.create_session()
    task = session.query(Task).filter(Task.id == context.user_data["selected_task_id"]).first()
    task.title = update.message.text
    session.commit()
    session.close()

    update.message.reply_text(CONTENT["message"]["task_title_edited"]["ru"])
    send_edit_mode_menu(update)

    return "edit_mode_handler"


def new_weekdays_handler(update, context):
    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["cancel"], "ru")

    if pushed_button == "cancel":
        send_edit_mode_menu(update)

        return "edit_mode_handler"

    weekdays_str = weekdays.get_weekdays_from_str(update.message.text, "ru")

    if not weekdays_str:
        update.message.reply_text(CONTENT["message"]["invalid_input"]["ru"])
        return "new_weekdays_handler"

    session = db_session.create_session()
    task = session.query(Task).filter(Task.id == context.user_data["selected_task_id"]).first()
    task.weekdays = weekdays_str
    session.commit()
    session.close()

    update.message.reply_text(CONTENT["message"]["task_weekdays_edited"]["ru"])
    send_edit_mode_menu(update)

    return "edit_mode_handler"


def edit_mode_handler(update, context):
    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["edit_task_menu"], "ru")

    if pushed_button == "back":
        if "page" not in context.user_data:
            context.user_data["page"] = 0

        update.message.reply_text(CONTENT["message"]["choice_task"]["ru"],
                                  reply_markup=keyboards.get_tasks_keyboard
                                  (update.message.from_user.id, "ru",
                                   page=context.user_data["page"]))
        return "choice_task_handler"

    elif pushed_button == "title":
        update.message.reply_text(CONTENT["message"]["write_task_title"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("cancel", "ru"))

        return "new_title_handler"

    elif pushed_button == "weekdays":
        update.message.reply_text(CONTENT["message"]["write_task_weekdays"]["ru"],
                                  reply_markup=keyboards.get_menu_keyboard("cancel", "ru"))

        return "new_weekdays_handler"

    else:
        update.message.reply_text(CONTENT["message"]["click_buttons"]["ru"])
        return "edit_mode_handler"


edit_task_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, choice_task_handler, pass_user_data=True)],

    states={
        "choice_task_handler": [
            MessageHandler(Filters.text, choice_task_handler, pass_user_data=True)],
        "edit_mode_handler": [MessageHandler(Filters.text, edit_mode_handler, pass_user_data=True)],
        "new_title_handler": [MessageHandler(Filters.text, new_title_handler, pass_user_data=True)],
        "new_weekdays_handler": [
            MessageHandler(Filters.text, new_weekdays_handler, pass_user_data=True)]
    },

    fallbacks=[],

    map_to_parent={
        ConversationHandler.END: "editor_menu"
    }
)
