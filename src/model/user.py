from dataclasses import dataclass
from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import ModelBase
from model.loan import Loan


@dataclass
class User(ModelBase):
    """
    A single registered user of the library. Note, this does not include Librarians.
    """
    __tablename__ = "registereduser"  # Avoids conflict with postgres builtin tables.

    id: int
    full_name: str
    loans: List[Loan]

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(200), unique=False)
    loans = relationship("Loan", viewonly=True)
