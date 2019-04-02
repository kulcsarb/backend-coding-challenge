import traceback
import socketio
import json
import logging 
from celery import Celery
from . import REDIS_URL, UNBABEL_API_KEY, UNBABEL_USERNAME
from .unbabel_api import UnbabelApi, UnauthorizedException, BadRequestException

LOGGER = logging.getLogger()

app = Celery('translator', broker=REDIS_URL)
sio = socketio.Server(client_manager=socketio.RedisManager(REDIS_URL), write_only=True)
unbabel = UnbabelApi(username=UNBABEL_USERNAME, api_key=UNBABEL_API_KEY, sandbox=True)


def event(channel, sid, message):
    sio.emit(channel, {'data': message}, room=sid)

def progress_event(sid, translation):
    event('progress', sid, json.dumps(translation.__dict__))

def error_event(sid, error):
    event('error', sid, error)


def refresh(sid, translation):
    if translation.status != "completed":
        get_translation.apply_async((sid, translation.uid), countdown=1)

@app.task
def translate(sid, text):
    try:
        translation = unbabel.post_translations(
                text=text,
                source_language="en", 
                target_language="es")                
        
        progress_event(sid, translation)

        refresh(sid, translation)

    except Exception as e:  
        LOGGER.error(traceback.format_exc())
        error_event(sid, 'TRANSLATION FAILED')
    

@app.task
def get_translation(sid, uid):    
    try:
        translation = unbabel.get_translation(uid)
        
        progress_event(sid, translation)

        refresh(sid, translation)
        
    except Exception as e:
        LOGGER.error(traceback.format_exc())        
        error_event(sid, 'STATUS FAILED')
    

if __name__ == '__main__':    
    app.start()
