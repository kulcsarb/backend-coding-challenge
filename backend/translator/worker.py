from __future__ import absolute_import
from celery.bin import worker
from .tasks import app
from . import db, init_logging, REDIS_URL
import logging

LOGGER = logging.getLogger('translator.worker')

if __name__ == '__main__':    
    init_logging()    
    db.init()    

    worker = worker.worker(app=app)    
    options = {
        'broker': REDIS_URL,
        'loglevel': 'INFO',
        'traceback': True,
    }

    worker.run(**options)

