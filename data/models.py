from sqlalchemy import orm
import sqlalchemy
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer)

    title = sqlalchemy.Column(sqlalchemy.String)
    days_of_the_week = sqlalchemy.Column(sqlalchemy.String)


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    language = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)