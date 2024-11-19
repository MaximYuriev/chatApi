import smtplib
from email.message import EmailMessage

from celery import Celery

from config import SMTP_USER, SMTP_HOST, SMTP_PORT, SMTP_PASSWORD
from services.user_redis import UserRedisService

celery = Celery("task", broker='redis://localhost:6379')


def get_email_message(email: str, user_id: int) -> EmailMessage:
    email_message = EmailMessage()
    email_message['Subject'] = 'Мессенджер'
    email_message['From'] = SMTP_USER
    email_message['To'] = email

    code_value = UserRedisService.generation_verify_code(user_id)

    email_message.set_content(
        '<div>'
        f'<h1>Код для подтверждения email: {code_value}</h1>'
        '</div>',
        subtype='html'
    )

    return email_message


@celery.task
def send_email_message(email: str, user_id: int):
    email_message = get_email_message(email, user_id)
    with smtplib.SMTP_SSL(host=SMTP_HOST, port=SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email_message)
