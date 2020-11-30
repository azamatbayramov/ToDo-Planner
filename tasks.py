from data.models import Task
from data import db_session

from days_of_the_week import get_today_day_of_the_week


def get_user_tasks(user_id, only_titles=False):
    session = db_session.create_session()
    tasks_list = session.query(Task).filter(Task.user_id == user_id).all()
    session.close()

    if only_titles:
        tasks_list = [task.title for task in tasks_list]
        tasks_list.sort()

    return tasks_list


def get_today_tasks(user_id):
    today_day_of_the_week = get_today_day_of_the_week()
    session = db_session.create_session()

    today_tasks = session.query(Task).filter(
        Task.user_id == user_id,
        Task.days_of_the_week.like(f"%{today_day_of_the_week}%")
    ).all()

    return today_tasks


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


def edit_task(task_id, title=None, days_of_the_week=None):
    if not title and not days_of_the_week:
        return False

    if title == "":
        return False

    if days_of_the_week == "":
        return False

    session = db_session.create_session()

    task = session.query(Task).filter(
        Task.id == task_id
    ).first()

    if title:
        task.title = title

    if days_of_the_week:
        task.days_of_the_week = days_of_the_week

    session.commit()
    session.close()

    return True


def delete_task(task_id):
    session = db_session.create_session()

    task = session.query(Task).filter(Task.id == task_id).first()

    session.delete(task)

    session.commit()
    session.close()
