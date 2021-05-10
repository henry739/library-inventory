from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from model.database import database


@dataclass
class Login(database.Model):
    __tablename__ = "login"

    id: int
    username: str
    password: str
    role: str

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    role = Column(String(32), nullable=False)
