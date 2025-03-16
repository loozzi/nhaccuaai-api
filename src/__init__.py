from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .api import __api
from .config import _config

app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

config = _config.getDevConfig()
env = config.ENV

app.config["SQLALCHEMY_DATABASE_URI"] = env.SQLALCHEMY_DATABASE_URI
app.env = env.ENV_NAME

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.register_blueprint(__api, url_prefix=_config.PREFIX_URL)
