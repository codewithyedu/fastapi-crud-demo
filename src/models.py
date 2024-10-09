from sqlalchemy import Column, String

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    password = Column(String)
