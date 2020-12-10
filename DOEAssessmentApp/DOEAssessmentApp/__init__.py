"""
app initialization
"""

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from DOEAssessmentApp import configs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('Logfiles.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'AhkjshjaskjJDJhshdjk'
if configs.prod_configs_from_file:
    for m in configs.prod_configs_from_file:
        app.config.update(m)

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

migrate = Migrate(app, db)
migrate.init_app(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

def create_app(config_map_list=None, blue_print_list=None):
    if blue_print_list:
        for bp in blue_print_list:
            app.register_blueprint(bp)

    return app
