import datetime

class Event:
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        return 'Event(subject={}, body={}, timestamp={})'.format(self.subject, self.body, self.timestamp)

class EventReceiver:
    def receive(self, event):
        pass

class EventManager:
    def __init__(self):
        self.receivers = []

    def register(self, receiver):
        self.receivers.append(receiver)

    def notify(self, event):
        for receiver in self.receivers:
            receiver.receive(event)

