from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from database.database import ModelBase


@dataclass
class Book(ModelBase):
    """
    A single copy of a book in the library's inventory.
    """
    __tablename__ = "book"

    id: int
    title: str
    author: str

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), unique=False)
    author = Column(String(200), unique=False)
