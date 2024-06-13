from . import database
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(150), unique=True)
    username = database.Column(database.String(150), unique=True)
    password = database.Column(database.String(150))
    date_created = database.Column(database.DateTime(timezone=True), default=func.now())


class Room(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(150), nullable=False)
    creator = database.Column(database.Integer, database.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    code = database.Column(database.Integer, nullable=False)
    date_created = database.Column(database.DateTime(timezone=True), default=func.now())


class Message(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    text = database.Column(database.Text, nullable=False)
    creator = database.Column(database.Integer, database.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    room = database.Column(database.Integer, database.ForeignKey('room.id', ondelete="CASCADE"), nullable=False)
    date_created = database.Column(database.DateTime(timezone=True), default=func.now())


class Membership(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    room_id = database.Column(database.Integer, database.ForeignKey('room.id', ondelete="CASCADE"), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = database.Column(database.DateTime(timezone=True), default=func.now())
