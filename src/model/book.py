from dataclasses import dataclass
from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import ModelBase
from model.loan import Loan


@dataclass
class Book(ModelBase):
    """
    A single copy of a book in the library's inventory.
    """

    __tablename__ = "book"

    id: int
    title: str
    author: str
    loans: List[Loan]

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), unique=False)
    author = Column(String(200), unique=False)
    loans = relationship("Loan", viewonly=True)
