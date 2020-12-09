"""
app initialization
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from DOEAssessmentApp import configs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AhkjshjaskjJDJhshdjk'
if configs.prod_configs_from_file:
    for m in configs.prod_configs_from_file:
        app.config.update(m)
db = SQLAlchemy(app)

def create_app(config_map_list=None, blue_print_list=None):
    if blue_print_list:
        for bp in blue_print_list:
            app.register_blueprint(bp)

    return app
