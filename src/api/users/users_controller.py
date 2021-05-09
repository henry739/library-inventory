import logging

from flask import jsonify, request, make_response, Response
from flask_restful import Resource
from jsonschema import ValidationError

from database.database import db_session
from model.user import User
from schema.schema_validator import SchemaValidator

logger = logging.Logger(__name__)


class UsersController(Resource):
    """
    Handles requests for user resources.
    """

    def __init__(self):
        self.validator = SchemaValidator("schema/user.schema.json")

    def post(self) -> Response:
        """
        Create a new user in the system.
        :return: User ID and 201 on successful creation, 400 if validation fails.
        """

        # Validate
        try:
            self.validator.validate(request.json)
            if "id" in request.json:
                return make_response("New records should not contain an ID", 400)

        except ValidationError:
            logger.exception(f"Request body failed validation against JsonSchema")
            return make_response("Invalid request format", 400)

        # Persist
        user = User(
            **request.json
        )  # Unexpected fields are disallowed during validation.
        db_session.add(user)
        db_session.commit()

        # Respond
        return make_response(str(user.id), 201)

    def get(self) -> Response:
        """
        Return all users in the system exactly matching the full_name GET parameter.
        :return: List of users and 200 on success
        """
        full_name = request.args.get("full_name")
        result = User.query.filter(User.full_name == full_name).all()

        return make_response(jsonify(result), 200)
