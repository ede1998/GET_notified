import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import mail as config
from input import events
import logging

logger = logging.getLogger(__name__)

def _create_message(receivers, subject, body):
    message = MIMEMultipart()
    message['From'] = config.sender
    message['To'] = ','.join(receivers)
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    return message

def _send(msg):
    with smtplib.SMTP(config.smtp_server, config.smtp_port) as s:
        s.starttls()
        s.ehlo()
        s.login(config.user, config.password)
        s.send_message(msg)

def _send_mail(receivers, subject, body):
    msg = _create_message(receivers, subject, body)
    _send(msg)

class SendMailEventReceiver(events.EventReceiver):
    def receive(self, event):
        logger.info('Sending mail')
        _send_mail(config.receivers, event.subject, event.body)
