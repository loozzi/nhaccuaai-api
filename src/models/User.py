from sqlalchemy import Column, Enum, Integer, String

from ..utils.enums import UserRole
from .Base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    oauth_id = Column(Integer, nullable=False, unique=True)
    email = Column(String, nullable=True, unique=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER.value)
    refresh_token = Column(String, nullable=True)

    def __init__(self, oauth_id: int, role: str):
        self.oauth_id = oauth_id
        self.role = role

    @classmethod
    def get_by_rf(cls, refresh_token: str, db=None):
        """
        Get a user by refresh token
        :param refresh_token: The refresh token
        :param db: Database session
        :return: The user
        """
        if db:
            return db.query(cls).filter(cls.refresh_token == refresh_token).first()
        else:
            return cls.query.filter_by(refresh_token=refresh_token).first()
