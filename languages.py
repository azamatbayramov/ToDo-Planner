"""Module for working with user's languages"""

from data.models import User
from data import db_session
from all_json import LANGUAGES


# Function for getting user language
def get_user_language(user_id=None, update=None, short=False):
    # If passed update, not user_id
    if update:
        user_id = update.message.from_user.id

    # Create database session
    session = db_session.create_session()

    # Get user information
    user = session.query(User).filter(User.telegram_id == user_id).first()

    # If user doesn't exist
    if not user:
        # Create new object for user with standard parameters
        new_user = User()
        new_user.telegram_id = user_id
        new_user.language_id = 0
        session.add(new_user)
        session.commit()
        user = new_user

    # Get user language
    language_id = user.language_id
    language = LANGUAGES[language_id]

    # Close database session
    session.close()

    # If passed "short"=True parameter, return short language
    if short:
        return language["short"]

    # Return language
    return language
