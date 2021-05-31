import datetime
from flask import jsonify
from DOEAssessmentApp import app
from flask_socketio import SocketIO
from DOEAssessmentApp.DOE_models.notification_model import Notification
from DOEAssessmentApp.DOE_models.notification_received_model import NotificationReceived
from DOEAssessmentApp.DOE_models.company_details_model import Companydetails
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.question_model import Question
from DOEAssessmentApp.DOE_models.assessment_model import Assessment
from DOEAssessmentApp.DOE_models.project_assignment_to_manager_model import Projectassignmenttomanager

socketio = SocketIO(app, cors_allowed_origins='*')


def get_notification_data(notification):
    notification_data = Notification.query.filter_by(event_name=notification['event_name'])

    if notification_data.first() is not None:
        empid = notification['empID']
        if notification['event_name'] == "ADDUSER":
            company_user_details = Companyuserdetails.query.filter_by(empid=empid).first()
            companyid = company_user_details.companyid
            company_details = Companydetails.query.filter_by(id=companyid).first()
            companyname = company_details.companyname
            app_notification = str(notification_data.first().app_notif_body).format(companyname=companyname)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "UPDATEUSER":
            company_user_details = Companyuserdetails.query.filter(
                Companyuserdetails.empid == empid).first()
            rolename = company_user_details.emprole
            app_notification = str(notification_data.first().app_notif_body).format(rolename=rolename)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "CHANGEPASSWORD":
            app_notification = notification_data.first().app_notif_body
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "PROJECTASSIGNMENT":
            projectid = notification['projectid']
            projectname = Project.query.filter_by(id=projectid)
            app_notification = str(notification_data.first().app_notif_body).format(
                projectname=projectname.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "PROJECTASSOCIATION":
            associate_status = notification['associate_status']
            projectid = notification['projectid']
            projectname = Project.query.filter(Project.id == projectid)
            if associate_status == 1:
                app_notification = str(notification_data.first().app_notif_body).format(
                    projectname=projectname.first().name, status="associated")
            else:
                app_notification = str(notification_data.first().app_notif_body).format(
                    projectname=projectname.first().name, status="disassociated")
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "ASSESSMENTASSIGNMENT":
            if notification['subfunc_id']:
                subfuncid = notification['subfunc_id']
                subfunc_data = Subfunctionality.query.filter_by(id=subfuncid).first()
                name = subfunc_data.name
            else:
                funcid = notification['func_id']
                func_data = Functionality.query.filter_by(id=funcid).first()
                name = func_data.name
            app_notification = str(notification_data.first().app_notif_body).format(name=name)

            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "ASSESSMENTASSOCIATIONTOTM":
            if notification['subfunc_id']:
                subfuncid = notification['subfunc_id']
                subfunc_data = Subfunctionality.query.filter_by(id=subfuncid).first()
                name = subfunc_data.name
            else:
                funcid = notification['func_id']
                func_data = Functionality.query.filter_by(id=funcid).first()
                name = func_data.name
            app_notification = str(notification_data.first().app_notif_body).format(
                employeeassignedstatus="associated",
                name=name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "SUBMITASSESSMENTWOREVIEW":
            isdraft = notification['isdraft']
            projid = notification['projectid']
            areaid = notification['area_id']
            funcid = notification['functionality_id']
            if "subfunc_id" in notification:
                subfuncid = notification['subfunc_id']
                dataforretake = Subfunctionality.query.filter_by(id=subfuncid).first()
                combination = str(empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
            else:
                dataforretake = Functionality.query.filter_by(id=funcid).first()
                combination = str(empid) + str(projid) + str(areaid) + str(funcid)
            assessment_data = Assessment.query.filter_by(combination=combination, active=1).first()
            assessmentid = assessment_data.id

            if isdraft == 0:
                rah = dataforretake.retake_assessment_days
                data = Assessment.query.filter_by(id=assessmentid)
                hours_added = datetime.timedelta(hours=rah)
                retakedatetime = data.first().assessmenttakendatetime + hours_added
                app_notification = str(notification_data.first().app_notif_body).format(date=str(retakedatetime.replace(
                    microsecond=0)))
                noti_dump = NotificationReceived(empid, app_notification, None)
                return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                                "role": notification_data.first().role})

        elif notification['event_name'] == "SUBMITASSESSMENTWREVIEWTOTM":
            # isdraft = notification['isdraft']
            # if isdraft == 0:
            app_notification = notification_data.first().app_notif_body
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "SAVEASDRAFTTOTM":
            # isdraft = notification['isdraft']
            app_notification = notification_data.first().app_notif_body
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "ASSESSMENTREJECTED":
            app_notification = notification_data.first().app_notif_body
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "ASSESSMENTACCEPTED":
            projid = notification['projectid']
            areaid = notification['area_id']
            funcid = notification['functionality_id']
            if "subfunc_id" in notification:
                subfuncid = notification['subfunc_id']
                dataforretake = Subfunctionality.query.filter_by(id=subfuncid).first()
                combination = str(empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
            else:
                dataforretake = Functionality.query.filter_by(id=funcid).first()
                combination = str(empid) + str(projid) + str(areaid) + str(funcid)
            assessment_data = Assessment.query.filter_by(combination=combination, active=1).first()
            assessmentid = assessment_data.id

            rah = dataforretake.retake_assessment_days
            data = Assessment.query.filter_by(id=assessmentid)
            hours_added = datetime.timedelta(hours=rah)
            retakedatetime = data.first().assessmenttakendatetime + hours_added
            app_notification = str(notification_data.first().app_notif_body).format(date=str(retakedatetime.replace(
                microsecond=0)))
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "DELETEPROJECTTOMANAGER":
            projectid = notification['projectid']
            projectname = Project.query.filter(Project.id == projectid)
            app_notification = str(notification_data.first().app_notif_body).format(
                projectname=projectname.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "ADDAREATOMANAGER":
            areaid = notification['areaid']
            areaname = Area.query.filter(Area.id == areaid)
            app_notification = str(notification_data.first().app_notif_body).format(
                areaname=areaname.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "DELETEAREATOMANAGER":
            areaid = notification['areaid']
            areaname = Area.query.filter(Area.id == areaid)
            app_notification = str(notification_data.first().app_notif_body).format(
                areaname=areaname.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "ADDFUNCTIONALITYTOMANAGER":
            funcid = notification['funcid']
            funcname = Functionality.query.filter(Functionality.id == funcid)
            app_notification = str(notification_data.first().app_notif_body).format(
                fname=funcname.first().name)

            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "UPDATEFUNCTIONALITYTOMANAGER":
            funcid = notification['funcid']
            funcname = Functionality.query.filter(Functionality.id == funcid)
            app_notification = str(notification_data.first().app_notif_body).format(
                fname=funcname.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "ADDSUBFUNCTIONALITYTOMANAGER":
            subfuncid = notification['subfuncid']
            subfuncname = Subfunctionality.query.filter(Subfunctionality.id == subfuncid)
            app_notification = str(notification_data.first().app_notif_body).format(
                subfuncname=subfuncname.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "UPDATESUBFUNCTIONALITYTOMANAGER":
            subfuncid = notification['subfuncid']
            subfuncname = Subfunctionality.query.filter(Subfunctionality.id == subfuncid)
            app_notification = str(notification_data.first().app_notif_body).format(
                subfuncname=subfuncname.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "DELETESUBFUNCTIONALITYTOMANAGER":
            subfuncid = notification['subfuncid']
            subfuncname = Subfunctionality.query.filter(Subfunctionality.id == subfuncid)
            app_notification = str(notification_data.first().app_notif_body).format(
                subfuncname=subfuncname.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "ADDQUESTIONTOMANAGER":
            questionid = notification['questionid']
            data = Question.query.filter_by(id=questionid)
            app_notification = str(notification_data.first().app_notif_body).format(
                questionname=data.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "UPDATEQUESTIONTOMANAGER":
            questionid = notification['questionid']
            data = Question.query.filter_by(id=questionid)
            app_notification = str(notification_data.first().app_notif_body).format(
                questionname=data.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "DELETEQUESTIONTOMANAGER":
            questionid = notification['questionid']
            data = Question.query.filter_by(id=questionid)
            app_notification = str(notification_data.first().app_notif_body).format(
                questionname=data.first().name)
            noti_dump = NotificationReceived(empid, app_notification, None)
            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        elif notification['event_name'] == "ASSESSMENTASSOCIATIONTOMANAGER":
            projectid = notification['projectid']
            managerdata = Projectassignmenttomanager.query.filter_by(project_id=projectid,
                                                                     status=1).first()
            assessmentid = notification['assessmentid']
            data = Assessment.query.filter_by(id=assessmentid)
            for user in data:
                subfunc_data = Subfunctionality.query.filter_by(
                    id=user.subfunctionality_id)
                func_data = Functionality.query.filter_by(id=user.functionality_id)
                if subfunc_data.first() is not None:
                    name = subfunc_data.first().name
                else:
                    name = func_data.first().name

                userdata = Companyuserdetails.query.filter_by(empid=managerdata.emp_id).first()
                managername = userdata.empname
                app_notification = str(notification_data.first().app_notif_body).format(managername=managername,
                                                                                        employeeassignedstatus="associated",
                                                                                        name=name)

                noti_dump = NotificationReceived(empid, app_notification, None)
                return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                                "role": notification_data.first().role})

        elif notification['event_name'] == "SUBMITASSESSMENTWREVIEWTOMANAGER":
            userdata = Companyuserdetails.query.filter_by(empid=empid).first()
            empname = userdata.empname
            app_notification = str(notification_data.first().app_notif_body).format(empname=empname)
            noti_dump = NotificationReceived(empid, app_notification, None)

            return jsonify({"empid": noti_dump.empid, "app_notification": noti_dump.app_notification,
                            "role": notification_data.first().role})

        # return jsonify({"empid": empid, "role": notification_data.first().role})
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
