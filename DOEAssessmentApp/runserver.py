"""
This script runs the PythonFlaskAPIForBlazorCln application using a development server.
"""

import DOEAssessmentApp
from DOEAssessmentApp import configs
from DOEAssessmentApp.views import emailconfig, rbac, companydetails, companyuserdetails

bp_list = [emailconfig, rbac, companydetails, companyuserdetails]

app = DOEAssessmentApp.create_app(config_map_list= configs.prod_configs_from_file,
                      blue_print_list=bp_list)
