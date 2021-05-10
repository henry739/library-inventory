import logging

from flask import jsonify, request, make_response, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from jsonschema import ValidationError

from api.auth.login_controller import LoginController
from model.database import database
from model.book import Book
from schema.schema_validator import SchemaValidator

logger = logging.Logger(__name__)


class BooksController(Resource):
    """
    Handles requests for book resources.
    """

    def __init__(self, schema_root):
        self.validator = SchemaValidator(f"{schema_root}/book.schema.json")

    @jwt_required()
    @LoginController.senior_authorization_required
    def post(self) -> Response:
        """
        Create a new book in the inventory.

        :return: Response containing the book ID and a status of 201 on success. Returns 400 on validation error.
        """
        try:
            self.validator.validate(request.json)
        except ValidationError:
            logger.exception(f"Request body failed validation against JsonSchema")
            return make_response("Invalid request format", 400)

        # Persist
        book = Book(**request.json)  # The above validation catches unwanted fields.
        database.session.add(book)
        database.session.commit()

        return make_response(str(book.id), 201)

    @jwt_required()
    def get(self) -> Response:
        """
        Return all books in the system with title matching the GET parameter. If not supplied, an empty list shall be
        returned.

        :return: Response containing a list of all matching books and a status of 201 on success.
        """
        title = request.args.get("title")
        result = Book.query.filter(Book.title == title).all()

        jsonified = jsonify(result)
        return make_response(jsonified, 200)
