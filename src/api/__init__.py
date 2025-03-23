from flask import Blueprint
from flask_restx import Api

__api = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    __api,
    version="1.0",
    title="NhacCuaAi API",
    description="NhacCuaAi API Documentation",
    doc="/docs/",
)

# Define namespaces
from .auth import auth_ns
from .genre import genre_ns

# Import namespaces
api.add_namespace(auth_ns)
api.add_namespace(genre_ns)
