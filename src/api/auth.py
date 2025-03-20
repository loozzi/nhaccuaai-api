from flask_restx import Namespace, Resource, fields

from src.controllers import AuthController
from src.utils import response

auth_ns = Namespace("auth", description="Authentication operations")

signin_model = auth_ns.model(
    "SignIn",
    {
        "token": fields.String(required=True, description="The token"),
    },
)

signup_model = auth_ns.model(
    "SignUp",
    {
        "token": fields.String(required=True, description="The token"),
    },
)

refresh_token_model = auth_ns.model(
    "RefreshToken",
    {
        "token": fields.String(required=True, description="The token"),
    },
)

route = {
    "sign-in": "/sign-in",
    "sign-up": "/sign-up",
    "refresh-token": "/refresh-token",
}


@auth_ns.route(route["sign-in"])
class SignInApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = AuthController()

    @auth_ns.expect(signin_model)
    @auth_ns.response(200, "Success")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Unauthorized")
    def post(self):
        try:
            return response(
                200,
                "Success",
                self.ctl.sign_in(auth_ns.payload["token"]),
            )
        except ValueError as e:
            return response(401, str(e))
        except Exception as e:
            return response(400, str(e))


@auth_ns.route(route["sign-up"])
class SignUpApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = AuthController()

    @auth_ns.expect(signup_model)
    @auth_ns.response(200, "Success")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Unauthorized")
    def post(self):
        try:
            return response(
                200,
                "Success",
                self.ctl.sign_up(auth_ns.payload["token"]),
            )
        except Exception as e:
            return response(400, str(e))


@auth_ns.route(route["refresh-token"])
class RefreshTokenApi(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctl = AuthController()

    @auth_ns.expect(refresh_token_model)
    @auth_ns.response(200, "Success")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Unauthorized")
    def post(self):
        try:
            return response(
                200,
                "Success",
                self.ctl.refresh_token(auth_ns.payload["token"]),
            )
        except ValueError as e:
            return response(401, str(e))
        except Exception as e:
            return response(400, str(e))
