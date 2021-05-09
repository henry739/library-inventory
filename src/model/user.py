from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from database.database import ModelBase


@dataclass
class User(ModelBase):
    """
    A single registered user of the library. Note, this does not include Librarians.
    """
    __tablename__ = "user"

    id: int
    full_name: str

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(200), unique=False)
