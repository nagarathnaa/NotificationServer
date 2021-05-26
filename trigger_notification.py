import requests
from flask import jsonify, json
from DOEAssessmentApp import app
from flask_socketio import SocketIO

socketio = SocketIO(app, cors_allowed_origins='*')


def get_notification_data(notification):
    eventlist = ["DELETEPROJECTTOMANAGER", "ADDAREATOMANAGER", "DELETEAREATOMANAGER", "ADDFUNCTIONALITYTOMANAGER",
                 "UPDATEFUNCTIONALITYTOMANAGER", "ADDSUBFUNCTIONALITYTOMANAGER", "UPDATESUBFUNCTIONALITYTOMANAGER",
                 "DELETESUBFUNCTIONALITYTOMANAGER", "ADDQUESTIONTOMANAGER", "UPDATEQUESTIONTOMANAGER",
                 "DELETEQUESTIONTOMANAGER", "ADDUSER", "UPDATEUSER", "CHANGEPASSWORD", "PROJECTASSIGNMENT",
                 "PROJECTASSOCIATION", "ASSESSMENTASSIGNMENT", "ASSESSMENTASSOCIATIONTOTM",
                 "ASSESSMENTASSOCIATIONTOMANAGER", "SUBMITASSESSMENTWOREVIEW", "SUBMITASSESSMENTWREVIEWTOTM",
                 "SUBMITASSESSMENTWREVIEWTOMANAGER", "SAVEASDRAFTTOTM", "ASSESSMENTREJECTED", "ASSESSMENTACCEPTED"]
    if notification['event_name'] in eventlist:
        API_ENDPOINT = 'http://127.0.0.1:5001/api/fetchnotificationdata/{}'.format(notification['event_name'])
        notification_data = requests.get(API_ENDPOINT)
        # print("get data", type(notification_data))
        print("get data", notification_data.text)
        json_data = json.loads(notification_data.text)
        print("json_data", json_data)
        print("role", json_data['data'][0]['role'])
        print("app_notif_body", json_data['data'][0]['app_notif_body'])

        return jsonify({"role": json_data['data'][0]['role'],
                        "app_notif_body": json_data['data'][0]['app_notif_body']})
    else:
        return jsonify({"message": "Notification event name not found"})


@socketio.on('notification')
def handle_message(notification):
    print('received message: ', notification)
    datas = get_notification_data(notification)
    # while True:
    socketio.emit('notification', datas,
                  broadcast=True, include_self=False)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5002)
    # app.run(debug=True, host='0.0.0.0', port=5001)
