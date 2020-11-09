from data.__all_models import users, tasks
from data import db_session


# Extracting classes
User = users.User
Task = tasks.Task

# Database initialization
db_session.global_init("db/database.sqlite")

