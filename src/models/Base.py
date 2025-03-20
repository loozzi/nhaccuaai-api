import datetime

from sqlalchemy import TIMESTAMP, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src import db


class Base(db.Model):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )
    updated_at: Mapped[datetime.date] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )

    def delete(self):
        self.is_deleted = True
        db.session.commit()
        return self

    def get(self, id: int):
        return self.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def __str__(self):
        return {
            c.name: (
                getattr(self, c.name).value
                if hasattr(getattr(self, c.name), "value")
                else getattr(self, c.name)
            )
            for c in self.__table__.columns
        }
