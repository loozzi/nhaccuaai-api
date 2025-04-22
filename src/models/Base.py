import datetime
from sqlalchemy import TIMESTAMP, Boolean, Integer, Column
from sqlalchemy.sql import func

from src import Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )

    def delete(self, db):
        self.is_deleted = True
        db.commit()
        return self

    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    def update(self, db, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.commit()
        db.refresh(self)
        return self

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def to_dict(self):
        def format_value(value):
            if hasattr(value, "value"):
                return value.value
            elif isinstance(value, (datetime.datetime, datetime.date)):
                return value.isoformat()
            else:
                return value

        return {
            c.name: format_value(getattr(self, c.name)) for c in self.__table__.columns
        }
