from telegram.ext import Updater
from data import db_session
from all_json import SETTINGS
from all_conversations import main_menu_conversation

# Database initialization
db_session.global_init("db/database.sqlite")


# Main function
def main():
    updater = Updater(token=SETTINGS["telegram_api_token"], use_context=True)

    dp = updater.dispatcher
    dp.add_handler(main_menu_conversation)

    updater.start_polling()
    updater.idle()


# Starting the main function
if __name__ == '__main__':
    main()
