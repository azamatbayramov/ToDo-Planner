from telegram.ext import MessageHandler, ConversationHandler, Filters
from all_json import SETTINGS, CONTENT, KEYBOARDS, MESSAGES
import keyboards
import days_of_the_week
import tasks
import languages


# Function for exiting from conversation
def exit_from_conversation(update):
    user_id = update.message.from_user.id
    language = languages.get_user_language(user_id)

    update.message.reply_text(
        CONTENT["signboard"]["editor_menu"][language["short"]],
        reply_markup=keyboards.get_menu_keyboard("editor_menu", language["short"])
    )

    return ConversationHandler.END


# Function - handler for title for a new task
def title_handler(update, context):
    user_id = update.message.from_user.id
    language = languages.get_user_language(user_id)

    pushed_button = keyboards.check_button(update, KEYBOARDS["static"]["cancel"], language["short"])

    if pushed_button == "cancel":
        return exit_from_conversation(update)

    task_titles_list = tasks.get_user_tasks(user_id, only_titles=True)

    if update.message.text in task_titles_list:
        update.message.reply_text(MESSAGES["task_exist"][language["short"]])
        return "title_handler"

    context.user_data["new_task"] = {}
    context.user_data["new_task"]["title"] = update.message.text

    update.message.reply_text(
        MESSAGES["write_task_days_of_the_week"][language["short"]],
        reply_markup=keyboards.get_menu_keyboard("cancel_back", language["short"])
    )

    return "days_of_the_week_handler"


# Function - handler for days of the week for a new task
def days_of_the_week_handler(update, context):
    user_id = update.message.from_user.id
    language = languages.get_user_language(user_id)

    pushed_button = keyboards.check_button(update,
                                           KEYBOARDS["static"]["cancel_back"],
                                           language["short"])

    if pushed_button == "cancel":
        return exit_from_conversation(update)

    if pushed_button == "back":
        update.message.reply_text(
            MESSAGES["write_task_title"][language["short"]],
            reply_markup=keyboards.get_menu_keyboard("cancel", language["short"])
        )

        return "title_handler"

    days_of_the_week_str = days_of_the_week.get_days_of_the_week_from_string(update.message.text,
                                                                             language["short"])

    if not days_of_the_week_str:
        update.message.reply_text(MESSAGES["invalid_input"][language["short"]])
        return "days_of_the_week_handler"

    context.user_data["new_task"]["days_of_the_week"] = "".join(days_of_the_week_str)

    tasks.add_task(user_id,
                   context.user_data["new_task"]["title"],
                   context.user_data["new_task"]["days_of_the_week"])

    context.user_data["new_task"] = {}

    update.message.reply_text(MESSAGES["task_added"][language["short"]])

    return exit_from_conversation(update)


# Conversation schema
add_task_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, title_handler, pass_user_data=True)],

    states={
        "title_handler": [MessageHandler(Filters.text, title_handler, pass_user_data=True)],
        "days_of_the_week_handler": [MessageHandler(Filters.text, days_of_the_week_handler,
                                                    pass_user_data=True)]
    },

    fallbacks=[],

    map_to_parent={
        ConversationHandler.END: "editor_menu"
    }
)
