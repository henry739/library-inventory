from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from model.database import Base


@dataclass
class Loan(Base):
    id: int
    started: datetime
    book_id: int
    registered_user_id: int

    __tablename__ = "loan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    started = Column(DateTime)
    book_id = Column(Integer, ForeignKey("book.id"))
    registered_user_id = Column(Integer, ForeignKey("registered_user.id"))
