from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional

from src.services import AuthService, FirebaseService
from src.utils.enums import UserRole
from src.utils.auth import create_access_token as create_jwt_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthController:
    def __init__(self):
        self.srv = AuthService()
        self.firebaseSrv = FirebaseService()

    def sign_in(self, token: str, db=None) -> dict:
        """
        Sign in a user
        :param token: The token
        :param db: Database session
        :return: The user data
        """
        user = self.srv.verify(token, db)
        user_id = user.get("user_id")
        return self.srv.generate_token(user_id, db)

    def sign_up(self, token: str, db=None) -> dict:
        """
        Sign up a user
        :param token: The token
        :param db: Database session
        :return: The user data
        """
        claims = self.firebaseSrv.verify(token)
        data = {
            "oauth_id": claims.get("oauth_id"),
            "role": UserRole.USER.value,
        }

        user = self.srv.sign_up(data, db)
        return self.srv.generate_token(user.id, db)

    def refresh_token(self, token: str, db=None) -> dict:
        """
        Refresh a token
        :param token: The token
        :param db: Database session
        :return: The user data
        """
        user = self.srv.verify(token, is_refresh_token=True, db=db)
        user_id = user.get("user_id")
        return self.srv.generate_token(user_id, db)
        
    def authenticate_user(self, email: str, password: str, db=None):
        """
        Authenticate a user with email and password
        :param email: The user email
        :param password: The user password
        :param db: Database session
        :return: User object if authentication is successful, otherwise None
        """
        user = self.srv.get_user_by_email(email, db)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user
    
    def verify_password(self, plain_password, hashed_password):
        """
        Verify password
        :param plain_password: The plain password
        :param hashed_password: The hashed password
        :return: True if passwords match, otherwise False
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        """
        Get password hash
        :param password: The plain password
        :return: The hashed password
        """
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """
        Create access token
        :param data: The data to encode in token
        :param expires_delta: The expiration time delta
        :return: The access token
        """
        return create_jwt_token(data, expires_delta)
