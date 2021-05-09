from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey

from database.database import ModelBase


@dataclass
class Loan(ModelBase):
    """ """

    __tablename__ = "loan"

    id: int
    due_date: datetime
    user_id: int
    book_id: int

    id = Column(Integer, primary_key=True, autoincrement=True)
    due_date = Column(DateTime())
    user_id = Column(Integer(), ForeignKey("registereduser.id"))
    book_id = Column(Integer(), ForeignKey("book.id"))
