"""
    Implementing a simple, scalable query translator backend for UnBabel's API
"""
__version__ = '0.1'

import os
import logging
import logging.config
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

PG_HOST = os.environ.get('PG_HOST', None)
PG_PORT = os.environ.get('PG_PORT', None)
PG_USER = os.environ.get('PG_USERNAME', None)
PG_PASSWORD = os.environ.get('PG_PASSWORD', None)
DATABASE = os.environ.get('DATABASE', None)

POSTGRESQL_URL = f'postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DATABASE}'

REDIS_URL = os.getenv("REDIS_URL")
UNBABEL_USERNAME = os.getenv("UNBABEL_USERNAME")
UNBABEL_API_KEY = os.getenv("UNBABEL_API_KEY")

ROOT_PATH = os.path.dirname(__file__)
CONFIG_DIR = os.path.join(ROOT_PATH, '.')

def init_logging():
     logging.config.fileConfig(os.path.join(CONFIG_DIR, 'logging.conf'))