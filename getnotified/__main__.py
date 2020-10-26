from input import flask
from sendmail import sendmail
from persistence import persistence
import logging

if __name__ == '__main__':
    mail_sender = sendmail.SendMailEventReceiver()
    persistence = persistence.PersistenceEventReceiver()
    flask.event_manager.register(mail_sender)
    flask.event_manager.register(persistence)
    logging.basicConfig(level=logging.DEBUG)
    flask.app.run()
