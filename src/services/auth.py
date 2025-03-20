from datetime import datetime, timedelta, timezone

import jwt

from src import env
from src.models import User


class AuthService:
    def __init__(self):
        pass

    def verify(self, token: str, is_refresh_token: bool = False) -> dict:
        """
        Verify a token
        :param token: The token to be verified
        :param is_refresh_token: If the token is a refresh token
        :return: The token claims if the token is valid, None otherwise
        """
        if is_refresh_token:
            user = User.get_by_rf(token)
            if not user:
                raise ValueError("Invalid token")

        try:
            return jwt.decode(
                token,
                env.JWT_SECRET,
                algorithms=["HS256"],
                options={"require": ["exp"]},
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def sign_up(self, data: dict) -> dict:
        """
        Sign up a new user
        :param data: The user data
        :return: The user data
        """
        user = User.query.filter_by(oauth_id=data.get("oauth_id")).first()
        if user:
            return user

        user = User(data.get("oauth_id"), data.get("role"))
        return user

    def generate_token(self, user_id: int) -> dict:
        """
        Generate a token
        :param user_id: The user ID
        :return: The generated token
        """
        # Generate access token
        data = {"user_id": user_id}
        data["iat"] = int(datetime.now(timezone.utc).timestamp())
        data["exp"] = int(
            datetime.now(timezone.utc)
            + timedelta(seconds=env.JWT_EXP_SECONDS).timestamp()
        )
        data["is_refresh_token"] = False
        access_token = jwt.encode(data, env.JWT_SECRET, algorithm="HS256")

        # Generate refresh token
        data["exp"] = int(
            datetime.now(timezone.utc)
            + timedelta(days=env.JWT_REFRESH_EXP_DAYS).timestamp()
        )
        data["is_refresh_token"] = True
        refresh_token = jwt.encode(data, env.JWT_SECRET, algorithm="HS256")

        # Save refresh token to user
        user: "User" = User.get(user_id)
        if user:
            user.update(refresh_token=refresh_token)
        else:
            raise ValueError("User not found")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
