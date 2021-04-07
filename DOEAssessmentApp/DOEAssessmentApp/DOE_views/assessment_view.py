from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.assessment_model import Assessment
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.question_model import Question
from DOEAssessmentApp.DOE_models.audittrail_model import Audittrail

assigningteammember = Blueprint('assigningteammember', __name__)


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@assigningteammember.route('/api/assigningteammember', methods=['GET', 'POST'])
def getandpost():
    try:
        result = []
        results = []
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "GET":
                    data = Assessment.query.filter_by(active=1).all()
                    for user in data:
                        userdata = Companyuserdetails.query.filter_by(empid=user.emp_id)
                        data_proj = Project.query.filter_by(id=user.projectid)
                        data_area = Area.query.filter_by(id=user.area_id)
                        data_func = Functionality.query.filter_by(id=user.functionality_id)
                        if userdata.first() is not None and data_proj.first() is not None and data_area.first() is not \
                                None and data_func.first() is not None:
                            if user.subfunctionality_id is not None:
                                data_subfunc = Subfunctionality.query.filter_by(id=user.subfunctionality_id)
                                if data_subfunc.first() is not None:
                                    json_data = {'id': user.id, 'emp_id': user.emp_id,
                                                 'emp_name': userdata.first().empname,
                                                 'project_id': user.projectid, 'project_name': data_proj.first().name,
                                                 'area_id': user.area_id, 'area_name': data_area.first().name,
                                                 'functionality_id': user.functionality_id,
                                                 'func_name': data_func.first().name,
                                                 'subfunctionality_id': user.subfunctionality_id,
                                                 'subfunc_name': data_subfunc.first().name,
                                                 'employeeassignedstatus': user.employeeassignedstatus,
                                                 'totalmaxscore': user.totalmaxscore,
                                                 'totalscoreachieved': user.totalscoreachieved,
                                                 'comment': user.comment, 'assessmentstatus': user.assessmentstatus,
                                                 'assessmenttakendatetime': user.assessmenttakendatetime,
                                                 'assessmentrevieweddatetime': user.assessmentrevieweddatetime,
                                                 'creationdatetime': user.creationdatetime,
                                                 'updationdatetime': user.updationdatetime}
                                    results.append(json_data)
                            else:
                                json_data = {'id': user.id, 'emp_id': user.emp_id, 'emp_name': userdata.first().empname,
                                             'project_id': user.projectid, 'project_name': data_proj.first().name,
                                             'area_id': user.area_id, 'area_name': data_area.first().name,
                                             'functionality_id': user.functionality_id,
                                             'func_name': data_func.first().name,
                                             'employeeassignedstatus': user.employeeassignedstatus,
                                             'totalmaxscore': user.totalmaxscore,
                                             'totalscoreachieved': user.totalscoreachieved,
                                             'comment': user.comment, 'assessmentstatus': user.assessmentstatus,
                                             'assessmenttakendatetime': user.assessmenttakendatetime,
                                             'assessmentrevieweddatetime': user.assessmentrevieweddatetime,
                                             'creationdatetime': user.creationdatetime,
                                             'updationdatetime': user.updationdatetime}
                                results.append(json_data)
                    return make_response(jsonify({"data": results})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    assessmentstatus = 'NEW'
                    team_empid = res['emp_id']
                    projid = res['projectid']
                    if 'functionality' in res and type(res['functionality']) is list:
                        funcid = res['functionality']
                        for f in funcid:
                            subfuncid = None
                            combination = str(team_empid) + str(projid) + str(f['area_id']) + str(f['functionality_id'])
                            adata = Assessment.query.filter_by(combination=combination)
                            if adata.first() is not None:
                                for a in adata:
                                    eachadata = Assessment.query.filter_by(id=a.id).first()
                                    eachadata.active = 0
                                    eachadata.modifiedby = session['empid']
                                    db.session.add(eachadata)
                                    db.session.commit()
                                    data = Assessment.query.filter_by(id=eachadata.id)
                                    for d in data:
                                        json_data = mergedict({'id': d.id},
                                                              {'emp_id': d.emp_id},
                                                              {'projectid': d.projectid},
                                                              {'area_id': d.area_id},
                                                              {'employeeassignedstatus': d.employeeassignedstatus},
                                                              {'combination': d.combination},
                                                              {'totalmaxscore': d.totalmaxscore},
                                                              {'totalscoreachieved': d.totalscoreachieved},
                                                              {'countoftotalquestions': d.countoftotalquestions},
                                                              {'comment': d.comment},
                                                              {'assessmentstatus': d.assessmentstatus},
                                                              {'assessmenttakendatetime': d.assessmenttakendatetime},
                                                              {
                                                                  'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                              {'assessmentretakedatetime': d.assessmentretakedatetime},
                                                              {'active': d.active},
                                                              {'creationdatetime': d.creationdatetime},
                                                              {'updationdatetime': d.updationdatetime},
                                                              {'createdby': d.createdby},
                                                              {'modifiedby': d.modifiedby})
                                        results.append(json_data)
                                    # region call audit trail method
                                    auditins = Audittrail("ASSESSMENT", "ADD", None, str(results[0]), session['empid'])
                                    db.session.add(auditins)
                                    db.session.commit()
                                    # end region

                            countoftotalquestions = Question.query.filter_by(proj_id=projid, area_id=f['area_id'],
                                                                             func_id=f['functionality_id']).count()
                            assessmentins = Assessment(team_empid, projid, f['area_id'], f['functionality_id'],
                                                       subfuncid, combination, assessmentstatus,
                                                       countoftotalquestions, session['empid'])
                            db.session.add(assessmentins)
                            db.session.commit()
                            data = Assessment.query.filter_by(id=assessmentins.id)
                            for d in data:
                                json_data = mergedict({'id': d.id},
                                                      {'emp_id': d.emp_id},
                                                      {'projectid': d.projectid},
                                                      {'area_id': d.area_id},
                                                      {'employeeassignedstatus': d.employeeassignedstatus},
                                                      {'combination': d.combination},
                                                      {'totalmaxscore': d.totalmaxscore},
                                                      {'totalscoreachieved': d.totalscoreachieved},
                                                      {'countoftotalquestions': d.countoftotalquestions},
                                                      {'comment': d.comment},
                                                      {'assessmentstatus': d.assessmentstatus},
                                                      {'assessmenttakendatetime': d.assessmenttakendatetime},
                                                      {'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                      {'assessmentretakedatetime': d.assessmentretakedatetime},
                                                      {'active': d.active},
                                                      {'creationdatetime': d.creationdatetime},
                                                      {'updationdatetime': d.updationdatetime},
                                                      {'createdby': d.createdby},
                                                      {'modifiedby': d.modifiedby})
                                results.append(json_data)
                            # region call audit trail method
                            auditins = Audittrail("ASSESSMENT", "ADD", None, str(results[0]), session['empid'])
                            db.session.add(auditins)
                            db.session.commit()
                            # end region
                            quesdata = Question.query.filter(Question.proj_id == projid,
                                                             Question.area_id == f['area_id'],
                                                             Question.func_id == f['functionality_id'])
                            for q in quesdata:
                                d = Question.query.filter_by(id=q.id)
                                d.first().islocked = 1
                                d.modifiedby = session['empid']
                                db.session.add(d.first())
                                db.session.commit()
                                data = Question.query.filter_by(id=d.first().id)
                                for d in data:
                                    json_data = mergedict({'id': d.id},
                                                          {'name': d.name},
                                                          {'answer_type': d.answer_type},
                                                          {'answers': d.answers},
                                                          {'maxscore': d.maxscore},
                                                          {'subfunc_id': d.subfunc_id},
                                                          {'func_id': d.func_id},
                                                          {'area_id': d.area_id},
                                                          {'proj_id': d.proj_id},
                                                          {'combination': d.combination},
                                                          {'mandatory': d.mandatory},
                                                          {'islocked': d.islocked},
                                                          {'isdependentquestion': d.isdependentquestion},
                                                          {'isdependentquestion': d.isdependentquestion},
                                                          {'creationdatetime': d.creationdatetime},
                                                          {'updationdatetime': d.updationdatetime},
                                                          {'createdby': d.createdby},
                                                          {'modifiedby': d.modifiedby})
                                    results.append(json_data)
                                # region call audit trail method
                                auditins = Audittrail("QUESTION", "ADD", None, str(results[0]), session['empid'])
                                db.session.add(auditins)
                                db.session.commit()
                            data = Assessment.query.filter_by(id=assessmentins.id).first()
                            userdata = Companyuserdetails.query.filter_by(empid=data.emp_id).first()
                            data_proj = Project.query.filter_by(id=data.projectid).first()
                            data_area = Area.query.filter_by(id=data.area_id).first()
                            data_func = Functionality.query.filter_by(id=data.functionality_id).first()
                            result.append({'id': data.id, 'emp_id': data.emp_id, 'emp_name': userdata.empname,
                                           'project_id': data.projectid, 'project_name': data_proj.name,
                                           'area_id': data.area_id, 'area_name': data_area.name,
                                           'functionality_id': data.functionality_id, 'func_name': data_func.name,
                                           'employeeassignedstatus': data.employeeassignedstatus,
                                           'totalmaxscore': data.totalmaxscore,
                                           'totalscoreachieved': data.totalscoreachieved,
                                           'comment': data.comment, 'assessmentstatus': data.assessmentstatus,
                                           'assessmenttakendatetime': data.assessmenttakendatetime,
                                           'assessmentrevieweddatetime': data.assessmentrevieweddatetime,
                                           'creationdatetime': data.creationdatetime,
                                           'updationdatetime': data.updationdatetime})
                    else:
                        areaid = res['area_id']
                        funcid = res['functionality_id']
                        if "subfunc_id" in res:
                            if type(res['subfunc_id']) is list:
                                subfuncid = res['subfunc_id']
                                for s in subfuncid:
                                    combination = str(team_empid) + str(projid) + str(areaid) + str(funcid) + str(s)
                                    adata = Assessment.query.filter_by(combination=combination)
                                    if adata.first() is not None:
                                        for a in adata:
                                            eachadata = Assessment.query.filter_by(id=a.id).first()
                                            eachadata.active = 0
                                            eachadata.modifiedby = session['empid']
                                            db.session.add(eachadata)
                                            db.session.commit()
                                            data = Assessment.query.filter_by(id=eachadata.id)
                                            for d in data:
                                                json_data = mergedict({'id': d.id},
                                                                      {'emp_id': d.emp_id},
                                                                      {'projectid': d.projectid},
                                                                      {'area_id': d.area_id},
                                                                      {
                                                                          'employeeassignedstatus': d.employeeassignedstatus},
                                                                      {'combination': d.combination},
                                                                      {'totalmaxscore': d.totalmaxscore},
                                                                      {'totalscoreachieved': d.totalscoreachieved},
                                                                      {
                                                                          'countoftotalquestions': d.countoftotalquestions},
                                                                      {'comment': d.comment},
                                                                      {'assessmentstatus': d.assessmentstatus},
                                                                      {
                                                                          'assessmenttakendatetime': d.assessmenttakendatetime},
                                                                      {
                                                                          'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                                      {
                                                                          'assessmentretakedatetime': d.assessmentretakedatetime},
                                                                      {'active': d.active},
                                                                      {'creationdatetime': d.creationdatetime},
                                                                      {'updationdatetime': d.updationdatetime},
                                                                      {'createdby': d.createdby},
                                                                      {'modifiedby': d.modifiedby})
                                                results.append(json_data)
                                            # region call audit trail method
                                            auditins = Audittrail("ASSESSMENT", "ADD", None, str(results[0]),
                                                                  session['empid'])
                                            db.session.add(auditins)
                                            db.session.commit()
                                            # end region
                                    countoftotalquestions = Question.query.filter_by(proj_id=projid,
                                                                                     area_id=areaid,
                                                                                     func_id=funcid,
                                                                                     subfunc_id=s).count()
                                    assessmentins = Assessment(team_empid, projid, areaid, funcid, s,
                                                               combination, assessmentstatus, countoftotalquestions,
                                                               session['empid'])
                                    db.session.add(assessmentins)
                                    db.session.commit()
                                    data = Assessment.query.filter_by(id=assessmentins.id)
                                    for d in data:
                                        json_data = mergedict({'id': d.id},
                                                              {'emp_id': d.emp_id},
                                                              {'projectid': d.projectid},
                                                              {'area_id': d.area_id},
                                                              {'employeeassignedstatus': d.employeeassignedstatus},
                                                              {'combination': d.combination},
                                                              {'totalmaxscore': d.totalmaxscore},
                                                              {'totalscoreachieved': d.totalscoreachieved},
                                                              {'countoftotalquestions': d.countoftotalquestions},
                                                              {'comment': d.comment},
                                                              {'assessmentstatus': d.assessmentstatus},
                                                              {'assessmenttakendatetime': d.assessmenttakendatetime},
                                                              {
                                                                  'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                              {'assessmentretakedatetime': d.assessmentretakedatetime},
                                                              {'active': d.active},
                                                              {'creationdatetime': d.creationdatetime},
                                                              {'updationdatetime': d.updationdatetime},
                                                              {'createdby': d.createdby},
                                                              {'modifiedby': d.modifiedby})
                                        result.append(json_data)
                                    # region call audit trail method
                                    auditins = Audittrail("ASSESSMENT", "ADD", None, str(result[0]), session['empid'])
                                    db.session.add(auditins)
                                    db.session.commit()
                                    # end region
                                    quesdata = Question.query.filter(Question.proj_id == projid,
                                                                     Question.area_id == areaid,
                                                                     Question.func_id == funcid,
                                                                     Question.subfunc_id == s)
                                    for q in quesdata:
                                        d = Question.query.filter_by(id=q.id)
                                        d.first().islocked = 1
                                        d.modifiedby = session['empid']
                                        db.session.add(d.first())
                                        db.session.commit()
                                        data = Question.query.filter_by(id=d.first().id)
                                        for d in data:
                                            json_data = mergedict({'id': d.id},
                                                                  {'name': d.name},
                                                                  {'answer_type': d.answer_type},
                                                                  {'answers': d.answers},
                                                                  {'maxscore': d.maxscore},
                                                                  {'subfunc_id': d.subfunc_id},
                                                                  {'func_id': d.func_id},
                                                                  {'area_id': d.area_id},
                                                                  {'proj_id': d.proj_id},
                                                                  {'combination': d.combination},
                                                                  {'mandatory': d.mandatory},
                                                                  {'islocked': d.islocked},
                                                                  {'isdependentquestion': d.isdependentquestion},
                                                                  {'isdependentquestion': d.isdependentquestion},
                                                                  {'creationdatetime': d.creationdatetime},
                                                                  {'updationdatetime': d.updationdatetime},
                                                                  {'createdby': d.createdby},
                                                                  {'modifiedby': d.modifiedby})
                                            result.append(json_data)
                                        # region call audit trail method
                                        auditins = Audittrail("QUESTION", "ADD", None, str(result[0]), session['empid'])
                                        db.session.add(auditins)
                                        db.session.commit()
                                    data = Assessment.query.filter_by(id=assessmentins.id).first()
                                    userdata = Companyuserdetails.query.filter_by(empid=data.emp_id).first()
                                    data_proj = Project.query.filter_by(id=data.projectid).first()
                                    data_area = Area.query.filter_by(id=data.area_id).first()
                                    data_func = Functionality.query.filter_by(id=data.functionality_id).first()
                                    data_subfunc = Subfunctionality.query.filter_by(
                                        id=data.subfunctionality_id).first()
                                    result.append(
                                        {'id': data.id, 'emp_id': data.emp_id, 'emp_name': userdata.empname,
                                         'project_id': data.projectid, 'project_name': data_proj.name,
                                         'area_id': data.area_id, 'area_name': data_area.name,
                                         'functionality_id': data.functionality_id,
                                         'func_name': data_func.name,
                                         'subfunctionality_id': data.subfunctionality_id,
                                         'subfunc_name': data_subfunc.name,
                                         'employeeassignedstatus': data.employeeassignedstatus,
                                         'totalmaxscore': data.totalmaxscore,
                                         'totalscoreachieved': data.totalscoreachieved,
                                         'comment': data.comment, 'assessmentstatus': data.assessmentstatus,
                                         'assessmenttakendatetime': data.assessmenttakendatetime,
                                         'assessmentrevieweddatetime': data.assessmentrevieweddatetime,
                                         'creationdatetime': data.creationdatetime,
                                         'updationdatetime': data.updationdatetime})
                            else:
                                subfuncid = res['subfunc_id']
                                combination = str(team_empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
                                adata = Assessment.query.filter_by(combination=combination)
                                if adata.first() is not None:
                                    for a in adata:
                                        eachadata = Assessment.query.filter_by(id=a.id).first()
                                        eachadata.active = 0
                                        eachadata.modifiedby = session['empid']
                                        db.session.add(eachadata)
                                        db.session.commit()
                                        data = Assessment.query.filter_by(id=eachadata.id)
                                        for d in data:
                                            json_data = mergedict({'id': d.id},
                                                                  {'emp_id': d.emp_id},
                                                                  {'projectid': d.projectid},
                                                                  {'area_id': d.area_id},
                                                                  {'employeeassignedstatus': d.employeeassignedstatus},
                                                                  {'combination': d.combination},
                                                                  {'totalmaxscore': d.totalmaxscore},
                                                                  {'totalscoreachieved': d.totalscoreachieved},
                                                                  {'countoftotalquestions': d.countoftotalquestions},
                                                                  {'comment': d.comment},
                                                                  {'assessmentstatus': d.assessmentstatus},
                                                                  {
                                                                      'assessmenttakendatetime': d.assessmenttakendatetime},
                                                                  {
                                                                      'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                                  {
                                                                      'assessmentretakedatetime': d.assessmentretakedatetime},
                                                                  {'active': d.active},
                                                                  {'creationdatetime': d.creationdatetime},
                                                                  {'updationdatetime': d.updationdatetime},
                                                                  {'createdby': d.createdby},
                                                                  {'modifiedby': d.modifiedby})
                                            result.append(json_data)
                                        # region call audit trail method
                                        auditins = Audittrail("ASSESSMENT", "ADD", None, str(result[0]),
                                                              session['empid'])
                                        db.session.add(auditins)
                                        db.session.commit()
                                        # end region
                                countoftotalquestions = Question.query.filter_by(proj_id=projid,
                                                                                 area_id=areaid,
                                                                                 func_id=funcid,
                                                                                 subfunc_id=subfuncid).count()
                                assessmentins = Assessment(team_empid, projid, areaid, funcid, subfuncid,
                                                           combination, assessmentstatus, countoftotalquestions,
                                                           session['empid'])
                                db.session.add(assessmentins)
                                db.session.commit()
                                data = Assessment.query.filter_by(id=assessmentins.id)
                                for d in data:
                                    json_data = mergedict({'id': d.id},
                                                          {'emp_id': d.emp_id},
                                                          {'projectid': d.projectid},
                                                          {'area_id': d.area_id},
                                                          {'employeeassignedstatus': d.employeeassignedstatus},
                                                          {'combination': d.combination},
                                                          {'totalmaxscore': d.totalmaxscore},
                                                          {'totalscoreachieved': d.totalscoreachieved},
                                                          {'countoftotalquestions': d.countoftotalquestions},
                                                          {'comment': d.comment},
                                                          {'assessmentstatus': d.assessmentstatus},
                                                          {'assessmenttakendatetime': d.assessmenttakendatetime},
                                                          {'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                          {'assessmentretakedatetime': d.assessmentretakedatetime},
                                                          {'active': d.active},
                                                          {'creationdatetime': d.creationdatetime},
                                                          {'updationdatetime': d.updationdatetime},
                                                          {'createdby': d.createdby},
                                                          {'modifiedby': d.modifiedby})
                                    result.append(json_data)
                                # region call audit trail method
                                auditins = Audittrail("ASSESSMENT", "ADD", None, str(result[0]), session['empid'])
                                db.session.add(auditins)
                                db.session.commit()
                                # end region
                                quesdata = Question.query.filter(Question.proj_id == projid,
                                                                 Question.area_id == areaid,
                                                                 Question.func_id == funcid,
                                                                 Question.subfunc_id == subfuncid)
                                for q in quesdata:
                                    d = Question.query.filter_by(id=q.id)
                                    d.first().islocked = 1
                                    d.first().modifiedby = session['empid']
                                    db.session.add(d.first())
                                    db.session.commit()
                                    data = Question.query.filter_by(id=d.first().id)
                                    for d in data:
                                        json_data = mergedict({'id': d.id},
                                                              {'name': d.name},
                                                              {'answer_type': d.answer_type},
                                                              {'answers': d.answers},
                                                              {'maxscore': d.maxscore},
                                                              {'subfunc_id': d.subfunc_id},
                                                              {'func_id': d.func_id},
                                                              {'area_id': d.area_id},
                                                              {'proj_id': d.proj_id},
                                                              {'combination': d.combination},
                                                              {'mandatory': d.mandatory},
                                                              {'islocked': d.islocked},
                                                              {'isdependentquestion': d.isdependentquestion},
                                                              {'isdependentquestion': d.isdependentquestion},
                                                              {'creationdatetime': d.creationdatetime},
                                                              {'updationdatetime': d.updationdatetime},
                                                              {'createdby': d.createdby},
                                                              {'modifiedby': d.modifiedby})
                                        result.append(json_data)
                                    # region call audit trail method
                                    auditins = Audittrail("QUESTION", "ADD", None, str(result[0]), session['empid'])
                                    db.session.add(auditins)
                                    db.session.commit()
                                data = Assessment.query.filter_by(id=assessmentins.id).first()
                                userdata = Companyuserdetails.query.filter_by(empid=data.emp_id).first()
                                data_proj = Project.query.filter_by(id=data.projectid).first()
                                data_area = Area.query.filter_by(id=data.area_id).first()
                                data_func = Functionality.query.filter_by(id=data.functionality_id).first()
                                data_subfunc = Subfunctionality.query.filter_by(id=data.subfunctionality_id).first()
                                result.append({'id': data.id, 'emp_id': data.emp_id, 'emp_name': userdata.empname,
                                               'project_id': data.projectid, 'project_name': data_proj.name,
                                               'area_id': data.area_id, 'area_name': data_area.name,
                                               'functionality_id': data.functionality_id,
                                               'func_name': data_func.name,
                                               'subfunctionality_id': data.subfunctionality_id,
                                               'subfunc_name': data_subfunc.name,
                                               'employeeassignedstatus': data.employeeassignedstatus,
                                               'totalmaxscore': data.totalmaxscore,
                                               'totalscoreachieved': data.totalscoreachieved,
                                               'comment': data.comment, 'assessmentstatus': data.assessmentstatus,
                                               'assessmenttakendatetime': data.assessmenttakendatetime,
                                               'assessmentrevieweddatetime': data.assessmentrevieweddatetime,
                                               'creationdatetime': data.creationdatetime,
                                               'updationdatetime': data.updationdatetime})
                        else:
                            subfuncid = None
                            combination = str(team_empid) + str(projid) + str(areaid) + str(funcid)
                            adata = Assessment.query.filter_by(combination=combination)
                            if adata.first() is not None:
                                for a in adata:
                                    eachadata = Assessment.query.filter_by(id=a.id).first()
                                    eachadata.active = 0
                                    eachadata.modifiedby = session['empid']
                                    db.session.add(eachadata)
                                    db.session.commit()
                                    data = Assessment.query.filter_by(id=eachadata.id)
                                    for d in data:
                                        json_data = mergedict({'id': d.id},
                                                              {'emp_id': d.emp_id},
                                                              {'projectid': d.projectid},
                                                              {'area_id': d.area_id},
                                                              {'employeeassignedstatus': d.employeeassignedstatus},
                                                              {'combination': d.combination},
                                                              {'totalmaxscore': d.totalmaxscore},
                                                              {'totalscoreachieved': d.totalscoreachieved},
                                                              {'countoftotalquestions': d.countoftotalquestions},
                                                              {'comment': d.comment},
                                                              {'assessmentstatus': d.assessmentstatus},
                                                              {'assessmenttakendatetime': d.assessmenttakendatetime},
                                                              {
                                                                  'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                              {'assessmentretakedatetime': d.assessmentretakedatetime},
                                                              {'active': d.active},
                                                              {'creationdatetime': d.creationdatetime},
                                                              {'updationdatetime': d.updationdatetime},
                                                              {'createdby': d.createdby},
                                                              {'modifiedby': d.modifiedby})
                                        result.append(json_data)
                                    # region call audit trail method
                                    auditins = Audittrail("ASSESSMENT", "ADD", None, str(result[0]), session['empid'])
                                    db.session.add(auditins)
                                    db.session.commit()
                                    # end region
                            countoftotalquestions = Question.query.filter_by(proj_id=projid, area_id=areaid,
                                                                             func_id=funcid).count()
                            assessmentins = Assessment(team_empid, projid, areaid, funcid, subfuncid,
                                                       combination, assessmentstatus, countoftotalquestions,
                                                       session['empid'])
                            db.session.add(assessmentins)
                            db.session.commit()
                            data = Assessment.query.filter_by(id=assessmentins.id)
                            for d in data:
                                json_data = mergedict({'id': d.id},
                                                      {'emp_id': d.emp_id},
                                                      {'projectid': d.projectid},
                                                      {'area_id': d.area_id},
                                                      {'employeeassignedstatus': d.employeeassignedstatus},
                                                      {'combination': d.combination},
                                                      {'totalmaxscore': d.totalmaxscore},
                                                      {'totalscoreachieved': d.totalscoreachieved},
                                                      {'countoftotalquestions': d.countoftotalquestions},
                                                      {'comment': d.comment},
                                                      {'assessmentstatus': d.assessmentstatus},
                                                      {'assessmenttakendatetime': d.assessmenttakendatetime},
                                                      {
                                                          'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                      {'assessmentretakedatetime': d.assessmentretakedatetime},
                                                      {'active': d.active},
                                                      {'creationdatetime': d.creationdatetime},
                                                      {'updationdatetime': d.updationdatetime},
                                                      {'createdby': d.createdby},
                                                      {'modifiedby': d.modifiedby})
                                result.append(json_data)
                            # region call audit trail method
                            auditins = Audittrail("ASSESSMENT", "ADD", None, str(result[0]), session['empid'])
                            db.session.add(auditins)
                            db.session.commit()
                            # end region
                            quesdata = Question.query.filter(Question.proj_id == projid,
                                                             Question.area_id == areaid,
                                                             Question.func_id == funcid)
                            for q in quesdata:
                                d = Question.query.filter_by(id=q.id)
                                d.first().islocked = 1
                                d.first().modifiedby = session['empid']
                                db.session.add(d.first())
                                db.session.commit()
                                data = Question.query.filter_by(id=d.first().id)
                                for d in data:
                                    json_data = mergedict({'id': d.id},
                                                          {'name': d.name},
                                                          {'answer_type': d.answer_type},
                                                          {'answers': d.answers},
                                                          {'maxscore': d.maxscore},
                                                          {'subfunc_id': d.subfunc_id},
                                                          {'func_id': d.func_id},
                                                          {'area_id': d.area_id},
                                                          {'proj_id': d.proj_id},
                                                          {'combination': d.combination},
                                                          {'mandatory': d.mandatory},
                                                          {'islocked': d.islocked},
                                                          {'isdependentquestion': d.isdependentquestion},
                                                          {'isdependentquestion': d.isdependentquestion},
                                                          {'creationdatetime': d.creationdatetime},
                                                          {'updationdatetime': d.updationdatetime},
                                                          {'createdby': d.createdby},
                                                          {'modifiedby': d.modifiedby})
                                    result.append(json_data)
                                # region call audit trail method
                                auditins = Audittrail("QUESTION", "ADD", None, str(result[0]), session['empid'])
                                db.session.add(auditins)
                                db.session.commit()
                                # end region
                            data = Assessment.query.filter_by(id=assessmentins.id).first()
                            userdata = Companyuserdetails.query.filter_by(empid=data.emp_id).first()
                            data_proj = Project.query.filter_by(id=data.projectid).first()
                            data_area = Area.query.filter_by(id=data.area_id).first()
                            data_func = Functionality.query.filter_by(id=data.functionality_id).first()
                            result.append({'id': data.id, 'emp_id': data.emp_id, 'emp_name': userdata.empname,
                                           'project_id': data.projectid, 'project_name': data_proj.name,
                                           'area_id': data.area_id, 'area_name': data_area.name,
                                           'functionality_id': data.functionality_id, 'func_name': data_func.name,
                                           'employeeassignedstatus': data.employeeassignedstatus,
                                           'totalmaxscore': data.totalmaxscore,
                                           'totalscoreachieved': data.totalscoreachieved,
                                           'comment': data.comment, 'assessmentstatus': data.assessmentstatus,
                                           'assessmenttakendatetime': data.assessmenttakendatetime,
                                           'assessmentrevieweddatetime': data.assessmentrevieweddatetime,
                                           'creationdatetime': data.creationdatetime,
                                           'updationdatetime': data.updationdatetime})
                    return make_response(jsonify({"msg": "Team Member successfully assigned.",
                                                  "data": result})), 201
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningteammember.route('/api/associateteammember/', methods=['PUT'])
def updateanddelete():
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
                rowid = res['rowid']
                data = Assessment.query.filter_by(id=rowid)
                for d in data:
                    json_data = mergedict({'id': d.id},
                                          {'emp_id': d.emp_id},
                                          {'projectid': d.projectid},
                                          {'area_id': d.area_id},
                                          {'employeeassignedstatus': d.employeeassignedstatus},
                                          {'combination': d.combination},
                                          {'totalmaxscore': d.totalmaxscore},
                                          {'totalscoreachieved': d.totalscoreachieved},
                                          {'countoftotalquestions': d.countoftotalquestions},
                                          {'comment': d.comment},
                                          {'assessmentstatus': d.assessmentstatus},
                                          {'assessmenttakendatetime': d.assessmenttakendatetime},
                                          {'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                          {'assessmentretakedatetime': d.assessmentretakedatetime},
                                          {'active': d.active},
                                          {'creationdatetime': d.creationdatetime},
                                          {'updationdatetime': d.updationdatetime},
                                          {'createdby': d.createdby},
                                          {'modifiedby': d.modifiedby})
                    results.append(json_data)
                asessmentdatabefore = results[0]
                results.clear()
                if data.first() is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'PUT':
                        associate_status = res['associate_status']
                        if associate_status == 1:
                            data.first().employeeassignedstatus = 1
                            data.first().modifiedby = session['empid']
                            db.session.add(data.first())
                            db.session.commit()
                            data = Assessment.query.filter_by(id=rowid)
                            for d in data:
                                json_data = mergedict({'id': d.id},
                                                      {'emp_id': d.emp_id},
                                                      {'projectid': d.projectid},
                                                      {'area_id': d.area_id},
                                                      {'employeeassignedstatus': d.employeeassignedstatus},
                                                      {'combination': d.combination},
                                                      {'totalmaxscore': d.totalmaxscore},
                                                      {'totalscoreachieved': d.totalscoreachieved},
                                                      {'countoftotalquestions': d.countoftotalquestions},
                                                      {'comment': d.comment},
                                                      {'assessmentstatus': d.assessmentstatus},
                                                      {'assessmenttakendatetime': d.assessmenttakendatetime},
                                                      {'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                      {'assessmentretakedatetime': d.assessmentretakedatetime},
                                                      {'active': d.active},
                                                      {'creationdatetime': d.creationdatetime},
                                                      {'updationdatetime': d.updationdatetime},
                                                      {'createdby': d.createdby},
                                                      {'modifiedby': d.modifiedby})
                                results.append(json_data)
                            assessmentdataafter = results[0]
                            # region call audit trail method
                            auditins = Audittrail("TEAM MEMBER ASSOCIATED STATUS", "UPDATE", str(asessmentdatabefore),
                                                  str(assessmentdataafter),
                                                  session['empid'])
                            db.session.add(auditins)
                            db.session.commit()
                            # end region
                            return make_response(jsonify({"msg": "Team Member associated successfully "})), 200
                        else:
                            data.first().employeeassignedstatus = 0
                            data.first().modifiedby = session['empid']
                            db.session.add(data.first())
                            db.session.commit()
                            data = Assessment.query.filter_by(id=rowid)
                            for d in data:
                                json_data = mergedict({'id': d.id},
                                                      {'emp_id': d.emp_id},
                                                      {'projectid': d.projectid},
                                                      {'area_id': d.area_id},
                                                      {'employeeassignedstatus': d.employeeassignedstatus},
                                                      {'combination': d.combination},
                                                      {'totalmaxscore': d.totalmaxscore},
                                                      {'totalscoreachieved': d.totalscoreachieved},
                                                      {'countoftotalquestions': d.countoftotalquestions},
                                                      {'comment': d.comment},
                                                      {'assessmentstatus': d.assessmentstatus},
                                                      {'assessmenttakendatetime': d.assessmenttakendatetime},
                                                      {'assessmentrevieweddatetime': d.assessmentrevieweddatetime},
                                                      {'assessmentretakedatetime': d.assessmentretakedatetime},
                                                      {'active': d.active},
                                                      {'creationdatetime': d.creationdatetime},
                                                      {'updationdatetime': d.updationdatetime},
                                                      {'createdby': d.createdby},
                                                      {'modifiedby': d.modifiedby})
                                results.append(json_data)
                            assessmentdataafter = results[0]
                            # region call audit trail method
                            auditins = Audittrail("TEAM MEMBER ASSOCIATED STATUS", "UPDATE", str(asessmentdatabefore),
                                                  str(assessmentdataafter),
                                                  session['empid'])
                            db.session.add(auditins)
                            db.session.commit()
                            # end region
                            return make_response(jsonify({"msg": "Team Member disassociated successfully"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningteammember.route('/api/fetchprojectassigntoteam/', methods=['POST'])
def fetchprojectassigntoteam():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    data = Assessment.query.distinct(Assessment.projectid).filter(Assessment.emp_id == emp_id,
                                                                                  Assessment.employeeassignedstatus
                                                                                  == 1)
                    lists = []
                    for user in data:
                        project_data = Project.query.filter(Project.id == user.projectid)
                        if project_data.first() is not None:
                            lists.append({'projectid': user.projectid, 'projectname': project_data.first().name})
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningteammember.route('/api/fetchareanametoteam/', methods=['POST'])
def fetchareanametoteam():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    projectid = res['projectid']
                    data = Assessment.query.distinct(Assessment.area_id).filter(Assessment.emp_id == emp_id,
                                                                                Assessment.projectid == projectid,
                                                                                Assessment.employeeassignedstatus == 1)

                    lists = []
                    for user in data:
                        area_data = Area.query.filter(Area.id == user.area_id)
                        if area_data.first() is not None:
                            lists.append({'area_id': user.area_id, 'area_name': area_data.first().name})
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningteammember.route('/api/fetchfunctionalitynametoteam/', methods=['POST'])
def fetchfunctionalitynametoteam():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    projectid = res['projectid']
                    area_id = res['area_id']
                    data = Assessment.query.distinct(Assessment.functionality_id).filter(Assessment.emp_id == emp_id,
                                                                                         Assessment.projectid
                                                                                         == projectid,
                                                                                         Assessment.area_id
                                                                                         == area_id,
                                                                                         Assessment.
                                                                                         employeeassignedstatus == 1)
                    lists = []
                    for user in data:
                        functionality_data = Functionality.query.filter(
                            Functionality.id == user.functionality_id)
                        if functionality_data.first() is not None:
                            lists.append(
                                {'functionality_id': user.functionality_id,
                                 'functionality_name': functionality_data.first().name})
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningteammember.route('/api/fetchSubfunctionalitynametoteam/', methods=['POST'])
def fetchsubfunctionalitynametoteam():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    projectid = res['projectid']
                    area_id = res['area_id']
                    functionality_id = res['functionality_id']
                    data = Assessment.query.distinct(Assessment.subfunctionality_id).filter(Assessment.emp_id == emp_id,
                                                                                            Assessment.projectid
                                                                                            == projectid,
                                                                                            Assessment.area_id
                                                                                            == area_id,
                                                                                            Assessment.functionality_id
                                                                                            == functionality_id,
                                                                                            Assessment.
                                                                                            employeeassignedstatus == 1)
                    lists = []
                    for user in data:
                        if user.subfunctionality_id is not None:
                            subfunc_data = Subfunctionality.query.filter(
                                Subfunctionality.id == user.subfunctionality_id)
                            if subfunc_data.first() is not None:
                                lists.append({'sucfunc_id': user.subfunctionality_id,
                                              'subfunc_name': subfunc_data.first().name})
                        else:
                            pass
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
