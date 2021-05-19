from flask import *
from DOEAssessmentApp import db
from flask_socketio import SocketIO
# from flask_socketio import ConnectionRefusedError
from .database_connection_for_socket import get_notification_data

socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('notification')
def handle_message(notification):
    print('received message: ', notification)
    datas = get_notification_data(notification)
    # while True:
    socketio.emit('notification', datas,
                  broadcast=True, include_self=False)


# @socketio.on('connect')
# def connect():
#     if not self.authenticate(request.args):
#         raise ConnectionRefusedError('unauthorized!')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5002)
    # app.run(debug=True, host='0.0.0.0', port=5001)
