from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


def setup_database(flask_app) -> None:
    """
    Create the database, using the context of the flask application. Doing this lazily helps mitigate issues with
    circular imports / dependencies.
    :param flask_app: Flask application to loan configuration from.
    """
    with flask_app.app_context():
        database.create_all()
