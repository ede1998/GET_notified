from peewee import SqliteDatabase, TextField, DateTimeField, Model
import datetime
from input import events, flask
import logging
import json
from flask_restful import Resource

db = SqliteDatabase('getnotified.db')


class BaseModel(Model):
    class Meta:
        database = db


class Event(BaseModel):
    subject = TextField()
    body = TextField()
    creation_time = DateTimeField(default=datetime.datetime.now)
    def to_dict(self):
        return { 'subject': self.subject, 'body': self.body, 'creation_time': self.creation_time.__str__() }

class PersistenceEventReceiver(events.EventReceiver):
    def __init__(self):
        db.connect()
        db.create_tables([Event])

    def __del__(self):
        db.close()

    def receive(self, event):
        Event.create(
            subject=event.subject,
            body=event.body,
            creation_time=event.timestamp)


class EventList(Resource):
    def get(self):
        db.connect()
        events = Event.select()
        serialized_events = [ event.to_dict() for event in events ]
        db.close()
        return serialized_events

flask.api.add_resource(EventList, '/list')
