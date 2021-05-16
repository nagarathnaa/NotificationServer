from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.notification_model import Notification
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.audittrail_model import Audittrail

notific = Blueprint('notific', __name__)

colsnotification = ['id', 'role', 'event_name', 'mail_subject', 'mail_body', 'app_notif_body', 'companyid',
                    'creationdatetime',
                    'updationdatetime', 'createdby', 'modifiedby']


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@notific.route('/api/viewnotification', methods=['GET', 'POST'])
def viewnotification():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "GET":
                    data = Notification.query.all()
                    result = [{col: getattr(d, col) for col in colsnotification} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    role = res['role']
                    event_name = res['event_name']
                    mail_subject = res['mail_subject']
                    mail_body = res['mail_body']
                    app_notif_body = res['app_notif_body']
                    companyid = res['companyid']
                    notification_data = Notification.query.filter(Notification.role == role,
                                                                  Notification.companyid == companyid).one_or_none()
                    if notification_data is None:
                        notifications = Notification(role, event_name, mail_subject, mail_body,
                                                     app_notif_body, companyid,
                                                     session['empid'])
                        db.session.add(notifications)
                        db.session.commit()
                        data = Notification.query.filter_by(id=notifications.id)
                        result = [{col: getattr(d, col) for col in colsnotification} for d in data]
                        # region call audit trail method
                        auditins = Audittrail("NOTIFICATION", "ADD", None, str(result[0]), session['empid'])
                        db.session.add(auditins)
                        db.session.commit()
                        # end region
                        return make_response(jsonify({"message": f"Notification data successfully inserted.",
                                                      "data": result[0]})), 201
                    else:
                        return make_response(jsonify({"message": f"Notification data already exists."})), 400
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@notific.route('/api/updelnotification/', methods=['POST', 'PUT', 'DELETE'])
def updelnotification():
    try:
        results = []
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                res = request.get_json(force=True)
                notificationid = res['notificationid']
                data = Notification.query.filter_by(id=notificationid)
                for nd in data:
                    json_data = mergedict({'id': nd.id},
                                          {'role': nd.role},
                                          {'event_name': nd.event_name},
                                          {'mail_subject': nd.mail_subject},
                                          {'mail_body': nd.mail_body},
                                          {'app_notif_body': nd.app_notif_body},
                                          {'companyid': nd.companyid},
                                          {'creationdatetime': nd.creationdatetime},
                                          {'updationdatetime': nd.updationdatetime},
                                          {'createdby': nd.createdby},
                                          {'modifiedby': nd.modifiedby})
                    results.append(json_data)
                notificationdatabefore = results[0]
                results.clear()
                if data.first() is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'POST':
                        for nd in data:
                            json_data = mergedict({'id': nd.id},
                                                  {'role': nd.role},
                                                  {'event_name': nd.event_name},
                                                  {'mail_subject': nd.mail_subject},
                                                  {'mail_body': nd.mail_body},
                                                  {'app_notif_body': nd.app_notif_body},
                                                  {'companyid': nd.companyid},
                                                  {'creationdatetime': nd.creationdatetime},
                                                  {'updationdatetime': nd.updationdatetime},
                                                  {'createdby': nd.createdby},
                                                  {'modifiedby': nd.modifiedby})
                            results.append(json_data)
                        return make_response(jsonify({"data": results[0]})), 200
                    elif request.method == 'PUT':
                        data.first().mail_subject = res['mail_subject']
                        data.first().mail_body = res['mail_body']
                        data.first().app_notif_body = res['app_notif_body']
                        data.first().modifiedby = session['empid']
                        db.session.add(data.first())
                        db.session.commit()
                        data = Notification.query.filter_by(id=notificationid)
                        for nd in data:
                            json_data = mergedict({'id': nd.id},
                                                  {'role': nd.role},
                                                  {'event_name': nd.event_name},
                                                  {'mail_subject': nd.mail_subject},
                                                  {'mail_body': nd.mail_body},
                                                  {'app_notif_body': nd.app_notif_body},
                                                  {'companyid': nd.companyid},
                                                  {'creationdatetime': nd.creationdatetime},
                                                  {'updationdatetime': nd.updationdatetime},
                                                  {'createdby': nd.createdby},
                                                  {'modifiedby': nd.modifiedby})
                            results.append(json_data)
                        notificationdataafter = results[0]
                        # region call audit trail method
                        auditins = Audittrail("NOTIFICATION", "UPDATE", str(notificationdatabefore),
                                              str(notificationdataafter),
                                              session['empid'])
                        db.session.add(auditins)
                        db.session.commit()
                        # end region
                        return make_response(jsonify({"message": f"NOTIFICATION with Features "
                                                                 f"successfully updated."})), 200
                    elif request.method == 'DELETE':
                        db.session.delete(data.first())
                        db.session.commit()
                        # region call audit trail method
                        auditins = Audittrail("NOTIFICATION", "DELETE", str(notificationdatabefore), None,
                                              session['empid'])
                        db.session.add(auditins)
                        db.session.commit()
                        return make_response(jsonify({"msg": f"NOTIFICATION with ID {notificationid} "
                                                             f"successfully deleted."})), 204
            else:
                return make_response(({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
