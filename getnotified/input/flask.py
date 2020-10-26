from flask import Flask, request
from werkzeug.exceptions import InternalServerError
from flask_restful import Resource, Api
from datetime import datetime
import threading
import time
import uuid
from . import events
import logging

tasks = {}

app = Flask(__name__)
api = Api(app)
event_manager = events.EventManager()


@app.before_first_request
def before_first_request():
    """Start a background thread that cleans up old tasks."""
    def clean_old_tasks():
        """
        This function cleans up old tasks from our in-memory data structure.
        """
        global tasks
        while True:
            # Only keep tasks that are running or that finished less than 5
            # minutes ago.
            five_min_ago = datetime.timestamp(datetime.utcnow()) - 5 * 60
            tasks = {task_id: task for task_id, task in tasks.items()
                     if 'completion_timestamp' not in task or
                     task['completion_timestamp'] > five_min_ago}
            time.sleep(60)

    thread = threading.Thread(target=clean_old_tasks)
    thread.start()


class Notification(Resource):
    def get(self):
        event = events.Event(
            request.args.get('subject', default='', type=str),
            request.args.get('body', default='', type=str))

        # Assign an id to the asynchronous task
        task_id = uuid.uuid4().hex

        def task_call(event):
            try:
                tasks[task_id]['return_value'] = event_manager.notify(event)
            except Exception:
                # The function raised an exception, so we set a 500 error
                tasks[task_id]['return_value'] = InternalServerError()
            finally:
                # We record the time of the response, to help in garbage
                # collecting old tasks
                tasks[task_id]['completion_timestamp'] = datetime.timestamp(
                    datetime.utcnow())

        # Record the task, and then launch it
        tasks[task_id] = {'task_thread': threading.Thread(
            target=task_call, args=(event,))}
        tasks[task_id]['task_thread'].start()

        return {k: v.__str__() for k, v in event.__dict__.items()}


api.add_resource(Notification, '/notification')
