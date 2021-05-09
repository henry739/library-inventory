from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool


# This allows SqlAlchemy to interact with our database. For testing purposes, currently an in-memory SQLite DB.
engine = create_engine(
    "sqlite://",
    poolclass=StaticPool,
    convert_unicode =True,
    connect_args={"check_same_thread": False}
)

# This session is used throughout the entire program, and is used directly by model classes.
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)


# SqlAlchemy provides a base class from which all models can derive.
ModelBase = declarative_base()
ModelBase.query = db_session.query_property()


def init_database():
    import model
    ModelBase.metadata.create_all(bind=engine)
