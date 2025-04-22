from datetime import datetime, timedelta, timezone

import jwt

from src import env
from src.models import User


class AuthService:
    def __init__(self):
        pass

    def verify(self, token: str, is_refresh_token: bool = False, db=None) -> dict:
        """
        Verify a token
        :param token: The token to be verified
        :param is_refresh_token: If the token is a refresh token
        :param db: Database session
        :return: The token claims if the token is valid, None otherwise
        """
        if is_refresh_token:
            if db:
                user = db.query(User).filter(User.refresh_token == token).first()
            else:
                user = User.query.filter_by(refresh_token=token).first()
                
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

    def sign_up(self, data: dict, db=None) -> dict:
        """
        Sign up a new user
        :param data: The user data
        :param db: Database session
        :return: The user data
        """
        if db:
            user = db.query(User).filter(User.oauth_id == data.get("oauth_id")).first()
        else:
            user = User.query.filter_by(oauth_id=data.get("oauth_id")).first()
            
        if user:
            return user

        user = User(data.get("oauth_id"), data.get("role"))
        
        if db:
            user.save(db)
        else:
            user.save()
            
        return user

    def generate_token(self, user_id: int, db=None) -> dict:
        """
        Generate a token
        :param user_id: The user ID
        :param db: Database session
        :return: The generated token
        """
        # Generate access token
        data = {"user_id": user_id}
        data["iat"] = int(datetime.now(timezone.utc).timestamp())
        data["exp"] = int(
            (datetime.now(timezone.utc)
            + timedelta(seconds=env.JWT_EXP_SECONDS)).timestamp()
        )
        data["is_refresh_token"] = False
        access_token = jwt.encode(data, env.JWT_SECRET, algorithm="HS256")

        # Generate refresh token
        data["exp"] = int(
            (datetime.now(timezone.utc)
            + timedelta(days=env.JWT_REFRESH_EXP_DAYS)).timestamp()
        )
        data["is_refresh_token"] = True
        refresh_token = jwt.encode(data, env.JWT_SECRET, algorithm="HS256")

        # Save refresh token to user
        if db:
            user = db.query(User).filter(User.id == user_id).first()
        else:
            user = User.query.get(user_id)
            
        if user:
            if db:
                user.update(db, refresh_token=refresh_token)
            else:
                user.update(refresh_token=refresh_token)
        else:
            raise ValueError("User not found")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    
    def get_user_by_email(self, email: str, db=None) -> User:
        """
        Get user by email
        :param email: User email
        :param db: Database session
        :return: User if found, None otherwise
        """
        if db:
            return db.query(User).filter(User.email == email).first()
        else:
            return User.query.filter_by(email=email).first()
