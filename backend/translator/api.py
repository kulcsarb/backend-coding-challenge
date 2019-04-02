import eventlet
eventlet.monkey_patch()
import logging 
import socketio
from . import tasks, db
from . import REDIS_URL, init_logging


LOGGER = logging.getLogger('translator.api')

sio = socketio.Server(async_mode='eventlet', \
            client_manager=socketio.RedisManager(REDIS_URL), \
            message_queue=REDIS_URL)

app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'translator/index.html'}
})


@sio.on('translate')
def message(sid, data):
    LOGGER.info('MESSAGE RECEIVED %s %s ' % (sid, data))
    tasks.translate.delay(sid, data['text'])


@sio.on('check')
def message(sid, data):
    LOGGER.info('MESSAGE RECEIVED %s %s ' % (sid, data))
    tasks.get_translation(sid, data['uid'])


if __name__ == '__main__':   
    init_logging()
    db.init()
    LOGGER.info("Starting WSGI server...")
    LOGGER.info("Redis at: %s" % REDIS_URL)
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)