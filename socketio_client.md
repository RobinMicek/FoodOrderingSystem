from flask import Flask, render_template
import socketio

app = Flask(__name__)

# Connect to the external Socket.IO server
external_server_url = 'https://external-server-url.com'  # Replace with the actual server URL
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('Connected to external Socket.IO server')

@sio.on('message_from_server')
def on_message(data):
    print('Received message from external server:', data)

@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from external Socket.IO server')

# Route to display messages (optional)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    sio.connect(external_server_url)
    app.run(debug=True)
