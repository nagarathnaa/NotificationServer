import datetime
from DOEAssessmentApp import app, db
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

        if notification['event_name'] == "ADDUSER":
            empid = notification['empID']
            company_user_details = Companyuserdetails.query.filter_by(empid=empid).first()
            companyid = company_user_details.companyid
            company_details = Companydetails.query.filter_by(id=companyid).first()
            companyname = company_details.companyname
            app_notification = str(notification_data.first().app_notif_body).format(companyname=companyname)
            noti_dump = NotificationReceived(empid, app_notification, None)

            db.session.add(noti_dump)
            db.session.commit()

            return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                    "role": notification_data.first().role}

        elif notification['event_name'] == "UPDATEUSER":
            empid = notification['empID']
            company_user_details = Companyuserdetails.query.filter(
                Companyuserdetails.empid == empid).first()
            rolename = company_user_details.emprole
            app_notification = str(notification_data.first().app_notif_body).format(rolename=rolename)
            noti_dump = NotificationReceived(empid, app_notification, None)
            db.session.add(noti_dump)
            db.session.commit()

            return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                    "role": notification_data.first().role}

        elif notification['event_name'] == "CHANGEPASSWORD":
            empid = notification['empID']
            app_notification = notification_data.first().app_notif_body
            noti_dump = NotificationReceived(empid, app_notification, None)
            db.session.add(noti_dump)
            db.session.commit()
            return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                    "role": notification_data.first().role}

        elif notification['event_name'] == "PROJECTASSIGNMENT":
            projectid = notification['projectid']
            projectname = Project.query.filter_by(id=projectid)
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=projectid)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                app_notification = str(notification_data.first().app_notif_body).format(
                    projectname=projectname.first().name)
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "PROJECTASSOCIATION":
            associate_status = notification['associate_status']
            projectid = notification['projectid']
            projectname = Project.query.filter(Project.id == projectid)
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=projectid)

            if associate_status == 1:
                app_notification = str(notification_data.first().app_notif_body).format(
                    status="associated", projectname=projectname.first().name)

            else:
                app_notification = str(notification_data.first().app_notif_body).format(
                    status="disassociated", projectname=projectname.first().name)

            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "ASSESSMENTASSIGNMENT":
            empid = notification['empID']
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
            db.session.add(noti_dump)
            db.session.commit()
            return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                    "role": notification_data.first().role}

        elif notification['event_name'] == "ASSESSMENTASSOCIATIONTOTM":
            empid = notification['empID']
            associate_status = notification['associate_status']
            if associate_status == 1:
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
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}
            else:
                if notification['subfunc_id']:
                    subfuncid = notification['subfunc_id']
                    subfunc_data = Subfunctionality.query.filter_by(id=subfuncid).first()
                    name = subfunc_data.name
                else:
                    funcid = notification['func_id']
                    func_data = Functionality.query.filter_by(id=funcid).first()
                    name = func_data.name
                app_notification = str(notification_data.first().app_notif_body).format(
                    employeeassignedstatus="disassociated",
                    name=name)
                noti_dump = NotificationReceived(empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "SUBMITASSESSMENTWOREVIEW":
            empid = notification['empID']
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
            data_proj = Project.query.filter_by(id=projid).first()
            if assessment_data is not None:
                assessmentid = assessment_data.id
                if data_proj.needforreview == 0:
                    if isdraft == 0:
                        rah = dataforretake.retake_assessment_days
                        data = Assessment.query.filter_by(id=assessmentid)
                        hours_added = datetime.timedelta(hours=rah)
                        retakedatetime = data.first().assessmenttakendatetime + hours_added
                        app_notification = str(notification_data.first().app_notif_body).format(
                            date=str(retakedatetime.replace(
                                microsecond=0)))
                        noti_dump = NotificationReceived(empid, app_notification, None)
                        db.session.add(noti_dump)
                        db.session.commit()
                        return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                                "role": notification_data.first().role}

        elif notification['event_name'] == "SUBMITASSESSMENTWREVIEWTOTM":
            empid = notification['empID']
            isdraft = notification['isdraft']
            projid = notification['projectid']
            data_proj = Project.query.filter_by(id=projid).first()
            if data_proj.needforreview == 0:
                if isdraft == 0:
                    app_notification = notification_data.first().app_notif_body
                    noti_dump = NotificationReceived(empid, app_notification, None)
                    db.session.add(noti_dump)
                    db.session.commit()
                    return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                            "role": notification_data.first().role}

        elif notification['event_name'] == "SAVEASDRAFTTOTM":
            empid = notification['empID']
            # isdraft = notification['isdraft']
            app_notification = notification_data.first().app_notif_body
            noti_dump = NotificationReceived(empid, app_notification, None)
            db.session.add(noti_dump)
            db.session.commit()
            return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                    "role": notification_data.first().role}

        elif notification['event_name'] == "ASSESSMENTREJECTED":
            empid = notification['empID']
            app_notification = notification_data.first().app_notif_body
            noti_dump = NotificationReceived(empid, app_notification, None)
            db.session.add(noti_dump)
            db.session.commit()
            return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                    "role": notification_data.first().role}

        elif notification['event_name'] == "ASSESSMENTACCEPTED":
            empid = notification['empID']
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
            db.session.add(noti_dump)
            db.session.commit()
            return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                    "role": notification_data.first().role}

        elif notification['event_name'] == "DELETEPROJECTTOMANAGER":
            projectid = notification['projectid']
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=projectid)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id

                app_notification = notification_data.first().app_notif_body
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "ADDAREATOMANAGER":
            projectid = notification['projectid']
            areaname = notification['areaname']
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=projectid)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                if manager_empid is not None:
                    app_notification = str(notification_data.first().app_notif_body).format(
                        areaname=areaname)
                    noti_dump = NotificationReceived(manager_empid, app_notification, None)
                    db.session.add(noti_dump)
                    db.session.commit()
                    return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                            "role": notification_data.first().role}

        elif notification['event_name'] == "DELETEAREATOMANAGER":
            projectid = notification['projectid']
            areaid = notification['areaid']
            areaname = Area.query.filter(Area.id == areaid).first()
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=projectid)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                app_notification = notification_data.first().app_notif_body
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "ADDFUNCTIONALITYTOMANAGER":
            func_name = notification['func_name']
            func_pro_id = notification['projectid']
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=func_pro_id)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id

                app_notification = str(notification_data.first().app_notif_body).format(
                    fname=func_name)

                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "UPDATEFUNCTIONALITYTOMANAGER":

            funcid = notification['funcid']
            func_pro_id = notification['projectid']
            funcname = Functionality.query.filter(Functionality.id == funcid).first()

            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=func_pro_id)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                app_notification = str(notification_data.first().app_notif_body).format(
                    fname=funcname.name)
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "ADDSUBFUNCTIONALITYTOMANAGER":
            subfunc_pro_id = notification['projectid']
            subfuncname = notification['subfunc_name']
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=subfunc_pro_id)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                app_notification = str(notification_data.first().app_notif_body).format(
                    subfuncname=subfuncname)
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "UPDATESUBFUNCTIONALITYTOMANAGER":
            subfunc_pro_id = notification['projectid']
            subfuncid = notification['subfuncid']
            subfuncname = Subfunctionality.query.filter(Subfunctionality.id == subfuncid).first()
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=subfunc_pro_id)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                app_notification = str(notification_data.first().app_notif_body).format(
                    subfuncname=subfuncname.name)
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "DELETESUBFUNCTIONALITYTOMANAGER":
            subfunc_pro_id = notification['projectid']
            subfuncid = notification['subfuncid']
            subfuncname = Subfunctionality.query.filter(Subfunctionality.id == subfuncid).first()
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=subfunc_pro_id)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                app_notification = notification_data.first().app_notif_body
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "ADDQUESTIONTOMANAGER":
            question_pro_id = notification['projectid']
            quesname = notification['QuestionName']
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=question_pro_id)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                app_notification = str(notification_data.first().app_notif_body).format(
                    questionname=quesname)
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "UPDATEQUESTIONTOMANAGER":
            question_pro_id = notification['projectid']
            questionid = notification['questionid']
            data = Question.query.filter_by(id=questionid).first()
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=question_pro_id)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                app_notification = str(notification_data.first().app_notif_body).format(
                    questionname=data.name)
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "DELETEQUESTIONTOMANAGER":
            question_pro_id = notification['projectid']
            questionid = notification['questionid']
            data = Question.query.filter_by(id=questionid).first()
            projectmanager = Projectassignmenttomanager.query.filter_by(project_id=question_pro_id)
            if projectmanager.first() is not None:
                manager_empid = projectmanager.first().emp_id
                app_notification = notification_data.first().app_notif_body
                noti_dump = NotificationReceived(manager_empid, app_notification, None)
                db.session.add(noti_dump)
                db.session.commit()
                return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                        "role": notification_data.first().role}

        elif notification['event_name'] == "ASSESSMENTASSOCIATIONTOMANAGER":
            empid = notification['empID']
            assessmentid = notification['assessmentid']
            associate_status = notification['associate_status']
            if associate_status == 1:
                data = Assessment.query.filter_by(id=assessmentid)
                for user in data:
                    subfunc_data = Subfunctionality.query.filter_by(
                        id=user.subfunctionality_id)
                    func_data = Functionality.query.filter_by(id=user.functionality_id)
                    if subfunc_data.first() is not None:
                        name = subfunc_data.first().name
                    else:
                        name = func_data.first().name

                    userdata = Companyuserdetails.query.filter_by(empid=empid).first()
                    empname = userdata.empname
                    app_notification = str(notification_data.first().app_notif_body).format(empname=empname,
                                                                                            employeeassignedstatus="associated",
                                                                                            name=name)

                    noti_dump = NotificationReceived(empid, app_notification, None)
                    db.session.add(noti_dump)
                    db.session.commit()
                    return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                            "role": notification_data.first().role}
            else:
                data = Assessment.query.filter_by(id=assessmentid)
                for user in data:
                    subfunc_data = Subfunctionality.query.filter_by(
                        id=user.subfunctionality_id)
                    func_data = Functionality.query.filter_by(id=user.functionality_id)
                    if subfunc_data.first() is not None:
                        name = subfunc_data.first().name
                    else:
                        name = func_data.first().name

                    userdata = Companyuserdetails.query.filter_by(empid=empid).first()
                    empname = userdata.empname
                    app_notification = str(notification_data.first().app_notif_body).format(empname=empname,
                                                                                            employeeassignedstatus="disassociated",
                                                                                            name=name)

                    noti_dump = NotificationReceived(empid, app_notification, None)
                    db.session.add(noti_dump)
                    db.session.commit()
                    return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                            "role": notification_data.first().role}

        elif notification['event_name'] == "SUBMITASSESSMENTWREVIEWTOMANAGER":
            empid = notification['empID']
            userdata = Companyuserdetails.query.filter_by(empid=empid).first()
            empname = userdata.empname
            app_notification = str(notification_data.first().app_notif_body).format(empname=empname)
            noti_dump = NotificationReceived(empid, app_notification, None)
            db.session.add(noti_dump)
            db.session.commit()

            return {"empid": noti_dump.empid, "app_notification": noti_dump.notification_content,
                    "role": notification_data.first().role}

    else:
        return {"message": "Notification event name not found"}


@socketio.on('notification')
def handle_message(notification):
    print('received message: ', notification)
    datas = get_notification_data(notification)
    # while True:
    socketio.emit('notification', datas,
                  broadcast=True, include_self=False)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5002)
