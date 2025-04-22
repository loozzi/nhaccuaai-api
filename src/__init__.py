import sys

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import _config

app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

config = _config.getProdConfig()
if len(sys.argv) > 1 and sys.argv[1] == "--dev":
    config = _config.getDevConfig()

env = config.ENV

app.config["SQLALCHEMY_DATABASE_URI"] = env.SQLALCHEMY_DATABASE_URI
app.env = env.ENV_NAME

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .api import __api
from .models import *

app.register_blueprint(__api, url_prefix=_config.PREFIX_URL)
