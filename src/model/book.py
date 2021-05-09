from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from model.database import Base


@dataclass
class Book(Base):
    id: int
    title: str
    author: str
    isbn: str

    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), unique=False)
    author = Column(String(200), unique=False)
    isbn = Column(String(16), unique=True)
