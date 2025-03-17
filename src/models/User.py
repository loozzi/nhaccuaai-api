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
