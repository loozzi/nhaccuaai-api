from src.services import AuthService, FirebaseService
from src.utils.enums import UserRole


class AuthController:
    def __init__(self):
        self.srv = AuthService()
        self.firebaseSrv = FirebaseService()

    def sign_in(self, token: str) -> dict:
        """
        Sign in a user
        :param token: The token
        :return: The user data
        """
        user = self.srv.verify(token)
        user_id = user.get("user_id")
        return self.srv.generate_token(user_id)

    def sign_up(self, token: str) -> dict:
        """
        Sign up a user
        :param token: The token
        :return: The user data
        """
        claims = self.firebaseSrv.verify(token)
        data = {
            "oauth_id": claims.get("oauth_id"),
            "role": UserRole.USER.value,
        }

        user = self.srv.sign_up(data)
        return self.srv.generate_token(user.id)

    def refresh_token(self, token: str) -> dict:
        """
        Refresh a token
        :param token: The token
        :return: The user data
        """
        user = self.srv.verify(token, is_refresh_token=True)
        user_id = user.get("user_id")
        return self.srv.generate_token(user_id)
