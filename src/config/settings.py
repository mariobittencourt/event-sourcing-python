from dotenv import load_dotenv
import os

path = os.path.dirname(os.path.realpath(__file__))
env_path = f'{path}/../../.env'
load_dotenv(dotenv_path=env_path, verbose=False)

DATABASE_NAME = os.getenv('DATABASE_NAME', 'payment_view.sqlite')
EVENT_STORE_USERNAME = os.getenv('EVENT_STORE_USERNAME', 'admin')
EVENT_STORE_PASSWORD = os.getenv('EVENT_STORE_PASSWORD', 'changeit')
PAYMENT_PROJECTION = 'customer'
DECLINE_PROJECTION = 'decline_code'
