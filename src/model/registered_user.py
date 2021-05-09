from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from model.database import Base


@dataclass
class RegisteredUser(Base):
    id: int
    full_name: str

    __tablename__ = "registered_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(200), unique=False)
