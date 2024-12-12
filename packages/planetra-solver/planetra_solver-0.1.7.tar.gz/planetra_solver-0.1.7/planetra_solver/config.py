import os

from dotenv import load_dotenv


load_dotenv()

LOGIN = os.environ.get('KS_LOGIN')
PASSWORD = os.environ.get('KS_PASSWORD')
PROJECT_UUID = os.environ.get('PROJECT_UUID')

DOMAIN_NAME = 'planetra.ru'
URL_PREFIX = 'learn'

