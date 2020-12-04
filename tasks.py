"""Module for working with tasks"""

from data.models import Task
from data import db_session

from days_of_the_week import get_today_day_of_the_week


def get_user_tasks(user_id, only_titles=False, today_tasks=False):
    """Get user tasks

    Keyword arguments:
    user_id -- user id for getting a tasks
    only_titles -- bool value for getting only titles of user tasks
    today_tasks -- bool value for getting today's tasks of user

    Return:
    List of user tasks
    """

    # Create new database session
    session = db_session.create_session()

    # Get list of the user tasks
    if not today_tasks:
        tasks_list = session.query(Task).filter(Task.user_id == user_id).all()
    else:
        # If today_tasks is True, get today's day and today's user tasks
        today_day_of_the_week = get_today_day_of_the_week()

        tasks_list = session.query(Task).filter(
            Task.user_id == user_id,
            Task.days_of_the_week.like(f"%{today_day_of_the_week}%")
        ).all()

    # Close session
    session.close()

    # If only_titles is True, get tasks names and sort list
    if only_titles:
        tasks_list = [task.title for task in tasks_list]
        tasks_list.sort()

    return tasks_list


def get_task_from_title(title, user_id, only_id=False):
    """Get a task from task title

    Keyword arguments:
    title -- task title for getting a task
    user_id -- user id for getting a task
    only_id -- bool value for getting only id of task

    Return:
    If task not found - False
    If only_id is False - Task object
    If only_id is True - task id
    """

    # Create new database session
    session = db_session.create_session()

    task = session.query(Task).filter(
        Task.title == title,
        Task.user_id == user_id
    ).first()

    # Close session
    session.close()

    # Return False if task not found
    if not task:
        return False

    # Return task id if only_id is True
    if only_id:
        return task.id

    # Return task if only_id is False
    return task


def add_task(user_id, title, days_of_the_week):
    """Add a new task to database

    Keyword arguments:
    user_id -- user id for adding a task
    title -- task title for adding a task
    days_of_the_week -- task days of the week for adding a task
    """

    # Create new task object, put details
    new_task = Task()
    new_task.user_id = user_id
    new_task.title = title
    new_task.days_of_the_week = days_of_the_week

    # Create database session, add new task, commit changes, close session
    session = db_session.create_session()
    session.add(new_task)
    session.commit()
    session.close()


def edit_task(task_id, title=None, days_of_the_week=None):
    """Edit a task in database

    Keyword arguments:
    task_id -- task id for editing a task
    title -- task title for editing a task
    days_of_the_week -- task days of the week for editing a task

    Return:
    If values is correct and editing successful - True
    Else - False
    """

    # Return False if no values passed
    if not title and not days_of_the_week:
        return False

    # Return False if title is empty string
    if title == "":
        return False

    # Return False if days_of_the_week is empty string
    if days_of_the_week == "":
        return False

    # Create new database session
    session = db_session.create_session()

    # Get task from database
    task = session.query(Task).filter(Task.id == task_id).first()

    # Edit task

    if title:
        task.title = title

    if days_of_the_week:
        task.days_of_the_week = days_of_the_week

    # Commit changes, close session
    session.commit()
    session.close()

    # Return True if editing is successful
    return True


def delete_task(task_id):
    """Delete a task from database

    Keyword arguments:
    task_id -- task id for deleting a task
    """

    # Create new database session
    session = db_session.create_session()

    # Get task from database, delete him
    task = session.query(Task).filter(Task.id == task_id).first()
    session.delete(task)

    # Commit changes, close session
    session.commit()
    session.close()
