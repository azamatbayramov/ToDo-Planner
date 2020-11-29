from data.models import User
from data import db_session
from all_json import LANGUAGES


def get_user_language(user_id=None, update=None, short=False):
    if update:
        user_id = update.message.from_user.id

    session = db_session.create_session()

    user = session.query(User).filter(User.telegram_id == user_id).first()

    if not user:
        new_user = User()
        new_user.telegram_id = user_id
        new_user.language_id = 0
        session.add(new_user)
        session.commit()
        user = new_user

    language_id = user.language_id
    language = LANGUAGES[language_id]

    session.close()

    if short:
        return language["short"]

    return language
