from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.notification_model import Notification


def get_notification_data(notification):
    eventlist = ["DELETEPROJECTTOMANAGER", "ADDAREATOMANAGER", "DELETEAREATOMANAGER", "ADDFUNCTIONALITYTOMANAGER",
                 "UPDATEFUNCTIONALITYTOMANAGER", "ADDSUBFUNCTIONALITYTOMANAGER", "UPDATESUBFUNCTIONALITYTOMANAGER",
                 "DELETESUBFUNCTIONALITYTOMANAGER", "ADDQUESTIONTOMANAGER", "UPDATEQUESTIONTOMANAGER",
                 "DELETEQUESTIONTOMANAGER", "ADDUSER", "UPDATEUSER", "CHANGEPASSWORD", "PROJECTASSIGNMENT",
                 "PROJECTASSOCIATION", "ASSESSMENTASSIGNMENT", "ASSESSMENTASSOCIATIONTOTM",
                 "ASSESSMENTASSOCIATIONTOMANAGER", "SUBMITASSESSMENTWOREVIEW", "SUBMITASSESSMENTWREVIEWTOTM",
                 "SUBMITASSESSMENTWREVIEWTOMANAGER", "SAVEASDRAFTTOTM", "ASSESSMENTREJECTED", "ASSESSMENTACCEPTED"]
    if notification['event_name'] in eventlist:
        notification_data = Notification.query.filter_by(event_name=notification['event_name']).first()
        return jsonify({"role": notification_data.role, "app_notif_body": notification_data.app_notif_body})
    else:
        return jsonify({"message": "Notification event name not found"})
