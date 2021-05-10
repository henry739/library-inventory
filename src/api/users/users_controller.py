import logging

from flask import jsonify, request, make_response, Response
from flask_restful import Resource
from jsonschema import ValidationError

from model.database import database
from model.user import User
from schema.schema_validator import SchemaValidator

logger = logging.Logger(__name__)


class UsersController(Resource):
    """
    Handles requests for user resources.
    """

    def __init__(self, schema_root):
        self.validator = SchemaValidator(f"{schema_root}/user.schema.json")

    def post(self) -> Response:
        """
        Create a new user in the system.

        :return: Response containing the user ID and a status of 201 on success. Returns 400 on validation error.
        """
        try:
            self.validator.validate(request.json)
        except ValidationError:
            logger.exception(f"Request body failed validation against JsonSchema")
            return make_response("Invalid request format", 400)

        # Persist
        user = User(**request.json)  # The above validation catches unwanted fields.
        database.session.add(user)
        database.session.commit()

        return make_response(str(user.id), 201)

    def get(self) -> Response:
        """
        Return all users in the system with full_name matching the GET parameter. If not supplied, an empty list
        shall be returned.

        :return: Response containing a list of matching users and a status of 200 on success.
        """
        full_name = request.args.get("full_name")
        result = User.query.filter(User.full_name == full_name).all()

        return make_response(jsonify(result), 200)
