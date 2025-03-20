from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..utils.enums import UserRole
from .Base import Base


class User(Base):
    __tablename__ = "users"
    oauth_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    role: Mapped[str] = mapped_column(
        Enum(UserRole), nullable=False, default=UserRole.USER.value
    )
    refresh_token: Mapped[str] = mapped_column(String, nullable=True)

    def __init__(self, oauth_id: int, role: str):
        self.oauth_id = oauth_id
        self.role = role
        self.save()
        return self

    def get_by_rf(self, refresh_token: str) -> "User":
        """
        Get a user by refresh token
        :param refresh_token: The refresh token
        :return: The user
        """
        return self.query.filter_by(refresh_token=refresh_token).first()
