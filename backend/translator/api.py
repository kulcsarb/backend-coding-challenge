import eventlet
eventlet.monkey_patch()
import logging 
import socketio
import json
from . import tasks, db
from . import REDIS_URL, init_logging


LOGGER = logging.getLogger('translator.api')

sio = socketio.Server(async_mode='eventlet', \
            client_manager=socketio.RedisManager(REDIS_URL), \
            message_queue=REDIS_URL)

app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'static/index.html'},
    '/Index.js': {'content_type': 'application/javascript', 'filename': 'static/Index.js'}
})


@sio.on('translate')
def message(sid, data):
    LOGGER.info('MESSAGE RECEIVED %s %s ' % (sid, data))
    data = json.loads(data)
    LOGGER.info(data[0])
    tasks.translate.delay(sid, data[0])


if __name__ == '__main__':   
    init_logging()
    db.init()
    LOGGER.info("Starting WSGI server...")
    LOGGER.info("Redis at: %s" % REDIS_URL)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)