from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey

from model.database import database


@dataclass
class Loan(database.Model):
    """ """

    __tablename__ = "loan"

    id: int
    due_date: datetime
    user_id: int
    book_id: int

    id = Column(Integer, primary_key=True, autoincrement=True)
    due_date = Column(DateTime(), nullable=False)
    user_id = Column(Integer(), ForeignKey("registereduser.id"), nullable=False)
    book_id = Column(Integer(), ForeignKey("book.id"), nullable=False)
