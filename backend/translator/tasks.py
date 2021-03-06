import traceback
import socketio
import json
import logging 
from celery import Celery
from celery.bin import worker

from . import REDIS_URL, UNBABEL_API_KEY, UNBABEL_USERNAME, init_logging
from .unbabel_api import UnbabelApi, UnauthorizedException, BadRequestException
from . import db

LOGGER = logging.getLogger('translator.tasks')

app = Celery('translator', broker=REDIS_URL)
sio = socketio.Server(client_manager=socketio.RedisManager(REDIS_URL), write_only=True)
unbabel = UnbabelApi(username=UNBABEL_USERNAME, api_key=UNBABEL_API_KEY, sandbox=True)


def event(channel, sid, message):
    LOGGER.warning(message)
    sio.emit(channel, message, room=sid)

def status_event(sid, translation):
    event('status', sid, json.dumps(translation.__dict__))

def error_event(sid, error):
    event('error', sid, error)

def refresh(sid, translation):
    if translation.status != "completed":
        get_translation.apply_async((sid, translation.uid), countdown=2)
 

@app.task
def translate(sid, text):                
    try:
        translation = unbabel.post_translations(
                text=text,
                source_language="en", 
                target_language="es"
        )            
        
        db.new_translation(sid, \
                translation.uid, \
                translation.text, \
                translation.source_language, \
                translation.target_language, \
                translation.status
        )

        status_event(sid, translation)

        refresh(sid, translation)

    except Exception as e:  
        LOGGER.error(traceback.format_exc())
        error_event(sid, 'TRANSLATION FAILED')
    

@app.task
def get_translation(sid, uid):        
    try:
        translation = unbabel.get_translation(uid)            

        db.update_translation(uid, \
                    translation.status, \
                    translation.translation
        )

        status_event(sid, translation)
        
        refresh(sid, translation)
    except ValueError:
        LOGGER.error(traceback.format_exc())        
        get_translation.apply_async((sid, uid), countdown=5)
        error_event(sid, e.message)
    except Exception as e:
        LOGGER.error(traceback.format_exc())        
        error_event(sid, 'STATUS FAILED')



