import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    days_of_week = sqlalchemy.Column(sqlalchemy.String)
