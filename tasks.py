from data.models import Task
from data import db_session


def get_user_tasks(user_id, generator=False):
    session = db_session.create_session()
    tasks_list = session.query(Task).filter(Task.user_id == user_id).all()
    session.close()

    if generator:
        for task in tasks_list:
            yield task
    else:
        return tasks_list


def add_task(user_id, title, weekdays):
    new_task = Task()
    new_task.user_id = user_id
    new_task.title = title
    new_task.weekdays = weekdays

    session = db_session.create_session()
    session.add(new_task)
    session.commit()
    session.close()
