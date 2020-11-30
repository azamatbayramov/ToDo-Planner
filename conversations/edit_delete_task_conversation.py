from telegram.ext import MessageHandler, ConversationHandler, Filters

from all_json import KEYBOARDS

from menu import send_editor_menu, send_edit_mode_menu, send_choice_tasks_menu
from tasks import get_user_tasks, get_task_id_from_title, edit_task, \
    delete_task
from days_of_the_week import get_days_of_the_week_from_string
from keyboards import get_menu_keyboard, check_button
from languages import get_user_language
from messages import get_message


# Function for exiting from conversation
def exit_from_conversation(update):
    send_editor_menu(update)
    return ConversationHandler.END


# Function - handler for task for editing/deleting
def choice_task_handler(update, context):
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    pushed_button = check_button(
        update, KEYBOARDS["static"]["cancel_back_next"], language
    )

    task_titles_list = get_user_tasks(user_id, only_titles=True)

    if update.message.text in task_titles_list:
        context.user_data["selected_task_id"] = \
            get_task_id_from_title(update.message.text)

        send_edit_mode_menu(update)

        return "edit_mode_handler"

    if pushed_button == "cancel":
        context.user_data["page"] = 0
        return exit_from_conversation(update)

    elif pushed_button == "next":
        if "page" in context.user_data:
            context.user_data["page"] += 1
        else:
            context.user_data["page"] = 1

        sending_result = send_choice_tasks_menu(
            update, context.user_data["page"]
        )

        if not sending_result:
            update.message.reply_text(get_message("click_buttons", language))
            context.user_data["page"] -= 1
            send_choice_tasks_menu(update, context.user_data["page"])

            return "choice_task_handler"

    elif pushed_button == "back":
        if "page" in context.user_data:
            if context.user_data["page"] > 0:
                context.user_data["page"] -= 1
                send_choice_tasks_menu(update, context.user_data["page"])

                return "choice_task_handler"

        update.message.reply_text(get_message("click_buttons", language))
        send_choice_tasks_menu(update)
        return "choice_task_handler"


# Function - handler for title for editing a task
def new_title_handler(update, context):
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    pushed_button = check_button(
        update, KEYBOARDS["static"]["cancel"], language
    )

    if pushed_button == "cancel":
        send_edit_mode_menu(update)

        return "edit_mode_handler"

    new_title = update.message.text

    task_titles_list = get_user_tasks(user_id, only_titles=True)

    if new_title in task_titles_list:
        update.message.reply_text(get_message("task_exist", language))
        return "new_title_handler"

    edit_result = edit_task(
        context.user_data["selected_task_id"],
        title=new_title
    )

    if edit_result:
        update.message.reply_text(get_message("task_title_edited", language))
        send_edit_mode_menu(update)
        return "edit_mode_handler"
    else:
        update.message.reply_text(get_message("invalid_input", language))
        return "new_title_handler"


# Function - handler for days of the week for editing a task
def new_days_of_the_week_handler(update, context):
    language = get_user_language(update=update, short=True)

    pushed_button = check_button(
        update, KEYBOARDS["static"]["cancel"], language
    )

    if pushed_button == "cancel":
        send_edit_mode_menu(update)

        return "edit_mode_handler"

    days_of_the_week_str = get_days_of_the_week_from_string(
        update.message.text, language
    )

    if not days_of_the_week_str:
        update.message.reply_text(get_message("invalid_input", language))
        return "new_days_of_the_week_handler"

    edit_result = edit_task(
        context.user_data["selected_task_id"],
        days_of_the_week=days_of_the_week_str
    )

    if edit_result:
        update.message.reply_text(
            get_message("task_days_of_the_week_edited", language)
        )
        send_edit_mode_menu(update)
        return "edit_mode_handler"
    else:
        update.message.reply_text(get_message("invalid_input", language))
        return "new_days_of_the_week_handler"


# Function - handler for mode of editing/deleting: edit title,
# edit days of the week, delete task
def edit_mode_handler(update, context):
    user_id = update.message.from_user.id
    language = get_user_language(user_id=user_id, short=True)

    pushed_button = check_button(
        update, KEYBOARDS["static"]["edit_task_menu"], language
    )

    if pushed_button == "back":
        if "page" not in context.user_data:
            context.user_data["page"] = 0

        send_choice_tasks_menu(update, context.user_data["page"])

        return "choice_task_handler"

    elif pushed_button == "title":
        update.message.reply_text(
            get_message("write_task_title", language),
            reply_markup=get_menu_keyboard("cancel", language)
        )

        return "new_title_handler"

    elif pushed_button == "days_of_the_week":
        update.message.reply_text(
            get_message("write_task_days_of_the_week", language),
            reply_markup=get_menu_keyboard("cancel", language)
        )

        return "new_days_of_the_week_handler"

    elif pushed_button == "delete":
        delete_task(context.user_data["selected_task_id"])

        update.message.reply_text(get_message("task_deleted", language))

        if get_user_tasks(user_id):
            send_choice_tasks_menu(update)
            context.user_data["page"] = 0

            return "choice_task_handler"

        else:
            send_editor_menu(update)

            return ConversationHandler.END

    else:
        update.message.reply_text(get_message("click_buttons", language))

        return "edit_mode_handler"


# Conversation scheme
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
