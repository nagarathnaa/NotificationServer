"""
app config initialization
"""

import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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
app.config['UPLOAD_FOLDER'] = 'static/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if configs.dev_configs_from_file:
    for m in configs.dev_configs_from_file:
        app.config.update(m)

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

