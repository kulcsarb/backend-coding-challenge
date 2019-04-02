from fabric.api import task, run
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import tasks.db as db
