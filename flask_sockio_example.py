from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from datetime import datetime
import random
import threading


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cnkddn#jkndf19722!'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    print('Here')
    return render_template('session.html')

@app.route('/test')
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')
    # socketio.emit('my response',  {'user_name': 'Server', 'message': f'{time.ctime()} test '})
    broadcast_event()
    return "Hello"

@socketio.on('message')
def handle_message(message):
    print('handle_message()')
    send(message)

@socketio.on('json')
def handle_json(json):
    print('handle_json()')
    send(json, json=True)

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    now = datetime.now()
    t = now.strftime("%Y-%m-%d %H:%M:%S")
    print('received my event: ' + str(json))
    socketio.emit('my response', {'Timestamp':t, 'user_name': 'Server', 'message':str(json)}, callback=messageReceived)

@socketio.on('connect')
def test_connect():
    now = datetime.now()
    t = now.strftime("%Y-%m-%d %H:%M:%S")
    print (f'Time: {time.ctime()}')
    socketio.emit('my response', {'Timestamp':t, 'user_name': 'Server', 'message': f'{time.ctime()} Connected '})
        
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


def broadcast_event():

    # current date and time
    now = datetime.now()
    t = now.strftime("%Y-%m-%d %H:%M:%S")
#
    print (f'Time: {time.ctime()}')
    socketio.emit('my response', {'Timestamp':t,  'user_name': 'Server', 'message': f'Dummy message {random.randint(0,10)}'})

@app.before_first_request   
def run_timer():
    
    def run_job():
        while True:
            broadcast_event()
            socketio.sleep(random.randint(1, 5))   
    socketio.start_background_task(target=run_job)

            
if __name__ == '__main__':
#    socketio.start_background_task(target=run_timer)
    socketio.run(app, host='0.0.0.0', debug=True)
