from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from model.database import Base


@dataclass
class Loan(Base):
    id: int
    started: datetime
    registered_user_id: int
    book_id: int

    __tablename__ = "loan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    started = Column(DateTime)
    registered_user_id = Column(Integer, ForeignKey("registered_user.id"))
    book_id = Column(Integer, ForeignKey("book.id"))
