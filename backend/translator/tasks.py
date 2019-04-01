import socketio
from celery import Celery

from . import REDIS_URL

app = Celery('translator', broker=REDIS_URL)

sio = socketio.Server(client_manager=socketio.RedisManager(REDIS_URL), write_only=True)

@app.task
def translate(msg):        
    print("--- SENDING RESULT TO: ", msg['sid'])    
    sio.emit('status', {'data': 'PENDING'}, room=msg['sid'])
    
    sio.emit('ping', {'data': 'PING'}, room=msg['sid'])    


if __name__ == '__main__':
    app.start()

# if __name__ == '__main__':
#     print("SENDING EVENT ON SocketIO")
#     mgr = socketio.RedisManager('redis://')
#     sio = socketio.Server(client_manager=mgr, write_only=True)    

#     sio.emit('status', {'data': 'PENDING'})
#     sio.emit('ping', {'data': 'PING'})
#     print('END.')
    
