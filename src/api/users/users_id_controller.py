import logging

from flask import jsonify, make_response, Response
from flask_restful import Resource

from database.database import db_session
from model.user import User

logger = logging.Logger(__name__)


class UsersIdController(Resource):
    """
    Handles requests for specific user resources.
    """

    def get(self, user_id: int) -> Response:
        """
        Return user with ID=user_id, if exists.

        :param user_id: ID of user to retrieve.
        :return: User matching ID and 200 on successful creation, 404 if not present
        """
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return make_response("User does not exist in the system", 404)

        return make_response(jsonify(user), 200)

    def delete(self, user_id: int) -> Response:
        """
        Delete the user with user_id if exists.

        :param user_id: ID of user to delete.
        :return: ID of the deleted user and 200 if successful, else 404.
        """
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return make_response("User does not exist in the system", 404)

        db_session.delete(user)
        db_session.commit()

        return make_response(jsonify(user.id), 200)