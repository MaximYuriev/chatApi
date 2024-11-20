import smtplib
from email.message import EmailMessage

from celery import Celery

from config import SMTP_USER, SMTP_HOST, SMTP_PORT, SMTP_PASSWORD

celery = Celery("task", broker='redis://localhost:6379')


def get_email_message(email: str, code_value: int) -> EmailMessage:
    email_message = EmailMessage()
    email_message['Subject'] = 'Мессенджер'
    email_message['From'] = SMTP_USER
    email_message['To'] = email

    email_message.set_content(
        '<div>'
        f'<h1>Код для подтверждения email: {code_value}</h1>'
        '</div>',
        subtype='html'
    )

    return email_message


@celery.task
def send_email_message(message_data: dict):
    email_message = get_email_message(**message_data)
    with smtplib.SMTP_SSL(host=SMTP_HOST, port=SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email_message)
