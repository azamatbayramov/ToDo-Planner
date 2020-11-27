from telegram.ext import MessageHandler, ConversationHandler, Filters
from all_json import CONTENT, KEYBOARDS, MESSAGES
from menu import send_editor_menu
from data import db_session
from data.models import Task
import keyboards
import days_of_the_week
import tasks


# Function for sending menu of conversation
def send_menu(update):
    update.message.reply_text(
        MESSAGES["choice_action"]["ru"],
        reply_markup=keyboards.get_menu_keyboard("edit_task_menu", "ru")
    )


# Function for exiting from conversation
def exit_from_conversation(update):
    send_editor_menu(update)
    return ConversationHandler.END


# Function - handler for task for editing/deleting
def choice_task_handler(update, context):
    pushed_button = keyboards.check_button(
        update, KEYBOARDS["static"]["cancel_back_next"], "ru"
    )

    task_titles_list = tasks.get_user_tasks(update.message.from_user.id,
                                            only_titles=True)

    if update.message.text in task_titles_list:
        context.user_data["selected_task_id"] = \
            tasks.get_task_id_from_title(update.message.text)

        send_menu(update)

        return "edit_mode_handler"

    if pushed_button == "cancel":
        return exit_from_conversation(update)

    elif pushed_button == "next":
        if "page" in context.user_data:
            context.user_data["page"] += 1
        else:
            context.user_data["page"] = 1

        keyboard = keyboards.get_tasks_keyboard(
            update.message.from_user.id, "ru", page=context.user_data["page"]
        )

        if keyboard:
            update.message.reply_text(MESSAGES["choice_task"]["ru"],
                                      reply_markup=keyboard)

            return "choice_task_handler"
        else:
            update.message.reply_text(MESSAGES["click_buttons"]["ru"])
            context.user_data["page"] -= 1
            return "choice_task_handler"

    elif pushed_button == "back":
        if "page" in context.user_data:
            if context.user_data["page"] > 0:
                context.user_data["page"] -= 1
                update.message.reply_text(
                    MESSAGES["choice_task"]["ru"],
                    reply_markup=keyboards.get_tasks_keyboard(
                        update.message.from_user.id, "ru",
                        page=context.user_data["page"]
                    )
                )

                return "choice_task_handler"

        update.message.reply_text(MESSAGES["click_buttons"]["ru"])
        return "choice_task_handler"


# Function - handler for title for editing a task
def new_title_handler(update, context):
    pushed_button = keyboards.check_button(
        update, KEYBOARDS["static"]["cancel"], "ru"
    )

    if pushed_button == "cancel":
        send_menu(update)

        return "edit_mode_handler"

    session = db_session.create_session()
    task = session.query(Task).filter(
        Task.id == context.user_data["selected_task_id"]
    ).first()

    task.title = update.message.text
    session.commit()
    session.close()

    update.message.reply_text(MESSAGES["task_title_edited"]["ru"])
    send_menu(update)

    return "edit_mode_handler"


# Function - handler for days of the week for editing a task
def new_days_of_the_week_handler(update, context):
    pushed_button = keyboards.check_button(
        update, KEYBOARDS["static"]["cancel"], "ru"
    )

    if pushed_button == "cancel":
        send_menu(update)

        return "edit_mode_handler"

    days_of_the_week_str = days_of_the_week.get_days_of_the_week_from_string(
        update.message.text, "ru"
    )

    if not days_of_the_week_str:
        update.message.reply_text(MESSAGES["invalid_input"]["ru"])
        return "new_days_of_the_week_handler"

    session = db_session.create_session()
    task = session.query(Task).filter(
        Task.id == context.user_data["selected_task_id"]
    ).first()

    task.days_of_the_week = days_of_the_week_str
    session.commit()
    session.close()

    update.message.reply_text(MESSAGES["task_days_of_the_week_edited"]["ru"])
    send_menu(update)

    return "edit_mode_handler"


# Function - handler for mode of editing/deleting: edit title,
# edit days of the week, delete task
def edit_mode_handler(update, context):
    pushed_button = keyboards.check_button(
        update, KEYBOARDS["static"]["edit_task_menu"], "ru"
    )

    if pushed_button == "back":
        if "page" not in context.user_data:
            context.user_data["page"] = 0

        update.message.reply_text(MESSAGES["choice_task"]["ru"],
                                  reply_markup=keyboards.get_tasks_keyboard
                                  (update.message.from_user.id, "ru",
                                   page=context.user_data["page"]))
        return "choice_task_handler"

    elif pushed_button == "title":
        update.message.reply_text(
            MESSAGES["write_task_title"]["ru"],
            reply_markup=keyboards.get_menu_keyboard("cancel", "ru")
        )

        return "new_title_handler"

    elif pushed_button == "days_of_the_week":
        update.message.reply_text(
            MESSAGES["write_task_days_of_the_week"]["ru"],
            reply_markup=keyboards.get_menu_keyboard("cancel", "ru")
        )

        return "new_days_of_the_week_handler"

    elif pushed_button == "delete":
        session = db_session.create_session()
        task = session.query(Task).filter(
            Task.id == context.user_data["selected_task_id"]
        ).first()

        session.delete(task)
        session.commit()
        session.close()

        update.message.reply_text(MESSAGES["task_deleted"]["ru"])

        if tasks.get_user_tasks(update.message.from_user.id):
            update.message.reply_text(MESSAGES["choice_task"]["ru"],
                                      reply_markup=keyboards.get_tasks_keyboard
                                      (update.message.from_user.id, "ru"))
            return "choice_task_handler"
        else:
            update.message.reply_text(
                CONTENT["signboard"]["editor_menu"]["ru"],
                reply_markup=keyboards.get_menu_keyboard("editor_menu", "ru")
            )
            return ConversationHandler.END

    else:
        update.message.reply_text(MESSAGES["click_buttons"]["ru"])
        return "edit_mode_handler"


# Conversation schema
edit_delete_task_conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.text, choice_task_handler, pass_user_data=True)
    ],

    states={
        "choice_task_handler": [
            MessageHandler(
                Filters.text, choice_task_handler, pass_user_data=True
            )
        ],
        "edit_mode_handler": [
            MessageHandler(
                Filters.text, edit_mode_handler, pass_user_data=True
            )
        ],
        "new_title_handler": [
            MessageHandler(
                Filters.text, new_title_handler, pass_user_data=True
            )
        ],
        "new_days_of_the_week_handler": [
            MessageHandler(
                Filters.text, new_days_of_the_week_handler, pass_user_data=True
            )
        ]
    },

    fallbacks=[],

    map_to_parent={
        ConversationHandler.END: "editor_menu"
    }
)
