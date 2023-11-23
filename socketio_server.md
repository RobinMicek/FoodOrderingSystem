from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Route for the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Event handler for when a client connects
@socketio.on('connect')
def handle_connect():
    print('A client has connected.')

# Event handler for joining a room
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('joined', {'room': room, 'message': 'You have joined the room.'}, room=room)

# Event handler for leaving a room
@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('left', {'room': room, 'message': 'You have left the room.'}, room=room)

# Event handler for custom message from the client in a specific room
@socketio.on('custom_message')
def handle_custom_message(data):
    message = data['message']
    room = data['room']
    emit('server_response', {'message': f'Server received in {room}: {message}'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
