from flask import Flask
from flask_socketio import SocketIO
# from flask_socketio import ConnectionRefusedError

app = Flask(__name__)

app.config['SECRET_KEY'] = 'testing!'
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('notification')
def handle_message(notification):
    print('received message: ', notification)
    # while True:
    socketio.emit('notification', notification,
                  broadcast=True, include_self=False)



# @socketio.on('connect')
# def connect():
#     if not self.authenticate(request.args):
#         raise ConnectionRefusedError('unauthorized!')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5002)
    # app.run(debug=True, host='0.0.0.0', port=5001)