"""
    Implementing a simple, scalable query translator backend for UnBabel's API
"""
__version__ = '0.1'

import os
import logging
import logging.config
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


POSTGRESQL_URL = os.getenv("POSTGRESQL_URL")
REDIS_URL = os.getenv("REDIS_URL")
UNBABEL_API_URL = os.getenv("UNBABEL_API_URL")
UNBABEL_USERNAME = os.getenv("UNBABEL_USERNAME")
UNBABEL_API_KEY = os.getenv("UNBABEL_API_KEY")

ROOT_PATH = os.path.dirname(__file__)
# PACKAGE_ROOT = os.path.join(ROOT_PATH, '..')
CONFIG_DIR = os.path.join(ROOT_PATH, '.')

def init_logging():
     logging.config.fileConfig(os.path.join(CONFIG_DIR, 'logging.conf'))