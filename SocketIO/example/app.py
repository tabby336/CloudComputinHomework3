#!/usr/bin/python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

NEWS_COUNT = 0
NEWS = {}


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/news')

"""
ADMIN
"""
@app.route('/admin')
def admin():
    return render_template('admin.html', async_mode=socketio.async_mode)

@socketio.on('admin_connect', namespace="/news")
def admin_connect(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', NEWS, namespace='/news')

@socketio.on('add_news', namespace='/news')
def add_news(message):
    global NEWS, NEWS_COUNT
    NEWS_COUNT += 1
    NEWS[NEWS_COUNT] = {'title': message['title'],
                        'body': message['body'],
                        'liked': ['ana', 'are'] }

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('added_news',
         {'count': NEWS_COUNT, 'data': NEWS[NEWS_COUNT]}, broadcast=True)

"""
USER
"""

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/news')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'blaa'}, namespace='/news')

@socketio.on('get_news', namespace='/news')
def get_news():
    emit('got_news', NEWS, namespace='/news')

@socketio.on('my_broadcast_event', namespace='/news')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/news')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/news')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/news')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/news')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/news')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping', namespace='/news')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/news')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', NEWS)


@socketio.on('disconnect', namespace='/news')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
