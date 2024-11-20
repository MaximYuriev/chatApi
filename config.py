from dotenv import load_dotenv
import os

load_dotenv()

COOKIES_KEY_NAME = os.environ.get('COOKIES_KEY_NAME')

POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

POSTGRES_DB_TEST = os.environ.get('POSTGRES_TEST_DB')

SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT'))

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = int(os.environ.get("REDIS_PORT"))

UVICORN_HOST = os.environ.get("UVICORN_HOST")
