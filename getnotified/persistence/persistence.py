from peewee import SqliteDatabase, TextField, DateTimeField, Model
import datetime
from input import events
import logging

db = SqliteDatabase('getnotified.db')


class BaseModel(Model):
    class Meta:
        database = db


class Event(BaseModel):
    subject = TextField()
    body = TextField()
    creation_time = DateTimeField(default=datetime.datetime.now)


class PersistenceEventReceiver(events.EventReceiver):
    def __init__(self):
        db.connect()
        db.create_tables([Event])

    def receive(self, event):
        Event.create(
            subject=event.subject,
            body=event.body,
            creation_time=event.timestamp)
