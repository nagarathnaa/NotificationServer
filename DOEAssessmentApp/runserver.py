"""
This script runs calls the create app method having endpoint blueprints as args
"""

import DOEAssessmentApp
from DOEAssessmentApp.DOE_views.email_configuration_view import emailconfig
from DOEAssessmentApp.DOE_views.rbac_view import rbac
from DOEAssessmentApp.DOE_views.company_details_view import companydetails
from DOEAssessmentApp.DOE_views.company_user_details_view import companyuserdetails
from DOEAssessmentApp.DOE_views.project_view import project
from DOEAssessmentApp.DOE_views.area_view import area

bp_list = [emailconfig, rbac, companydetails, companyuserdetails, project, area]

app = DOEAssessmentApp.create_app(blue_print_list=bp_list)
