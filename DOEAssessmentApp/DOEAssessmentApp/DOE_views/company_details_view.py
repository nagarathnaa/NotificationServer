import uuid
from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.company_details_model import Companydetails
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from werkzeug.security import generate_password_hash

companydetails = Blueprint('companydetails', __name__)

colscompanydetails = ['id', 'companyname', 'registeredaddress', 'billingaddress', 'gstortaxnumber', 'registrationkey',
                      'registrationkeyvalidated', 'creationdatetime', 'updationdatetime']


@companydetails.route('/api/companydetails', methods=['GET', 'POST'])
def companydetail():
    try:
        if request.method == "GET":
            data = Companydetails.query.all()
            result = [{col: getattr(d, col) for col in colscompanydetails} for d in data]
            return jsonify({"data": result})
        elif request.method == "POST":
            res = request.get_json(force=True)
            cname = res['CompanyName']
            regadrs = res['RegisteredAddress']
            billadrs = res['BillingAddress']
            gstno = res['GstorTaxNumber']
            regkey = str(uuid.uuid4())
            eid = res['EmployeeId']
            ename = res['EmployeeName']
            erole = res['EmployeeRole']
            email = res['EmployeeEmail']
            existing_company = Companydetails.query.filter(Companydetails.companyname == cname).one_or_none()
            if existing_company is None:
                compdet = Companydetails(cname, regadrs, billadrs, gstno, regkey)
                db.session.add(compdet)
                db.session.commit()
                compuserdet = Companyuserdetails(eid, ename, erole, email,
                                                 generate_password_hash(res['EmployeePassword']), compdet.id)
                db.session.add(compuserdet)
                db.session.commit()
                return jsonify({"message": f"Company details with Company Name {cname} successfully inserted."})
            else:
                return jsonify({"message": f"Company details with Company Name {cname} already exists."})
    except Exception as e:
        return e
