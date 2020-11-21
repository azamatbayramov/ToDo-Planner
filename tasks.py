from data.models import Task
from data import db_session


def get_user_tasks(user_id, only_titles=False):
    session = db_session.create_session()
    tasks_list = session.query(Task).filter(Task.user_id == user_id).all()
    session.close()

    if only_titles:
        tasks_list = [task.title for task in tasks_list]
        tasks_list.sort()

    return tasks_list


def get_task_id_from_title(title=None):
    session = db_session.create_session()
    task_id = session.query(Task).filter(Task.title == title).first().id
    session.close()

    return task_id


def add_task(user_id, title, weekdays):
    new_task = Task()
    new_task.user_id = user_id
    new_task.title = title
    new_task.days_of_the_week = weekdays

    session = db_session.create_session()
    session.add(new_task)
    session.commit()
    session.close()
