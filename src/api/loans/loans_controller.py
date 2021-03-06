import logging
from datetime import datetime, timedelta

from flask import jsonify, request, make_response, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from jsonschema import ValidationError

from model.database import database
from model.book import Book
from model.loan import Loan
from model.user import User
from schema.schema_validator import SchemaValidator

logger = logging.Logger(__name__)


class LoansController(Resource):
    """
    Handles requests for loan resources.
    """

    def __init__(self, schema_root):
        self._loan_length = 7
        self.validator = SchemaValidator(f"{schema_root}/loan.schema.json")

    def generate_due_date(self) -> datetime:
        """
        Generate a date-time in the future.

        :return: Datetime in the future, determined by library policy.
        """
        now = datetime.utcnow()
        return now + timedelta(self._loan_length)

    def can_user_borrow_book(self, user_id: int, book_id: int) -> (bool, str):
        """
        Determine if the specified user can loan the specified book.

        :param user_id: ID of the user who wants to borrow the book.
        :param book_id: ID of the book the user wants to borrow.
        :return: True if the user is able and allowed to borrow the book, False otherwise. Error message if fails.
        """
        user = User.query.filter(User.id == user_id).first()
        book = Book.query.filter(Book.id == book_id).first()

        if user is None:
            return False, "Cannot create loan. User does not exist in the system."

        if book is None:
            return False, "Cannot create loan. Book does not exist in the system."

        if len(user.loans) >= 4:
            return False, "Cannot create loan. User has four or more active loans."

        now = datetime.utcnow()
        if any(loan.due_date < now for loan in user.loans):
            return False, "Cannot create loan. User is overdue on one or more loans."

        if len(book.loans) > 0:
            return False, "Cannot create loan. Book is part of an active loan."

        return True, None

    @jwt_required()
    def post(self) -> Response:
        """
        Create a new loan in the system.

        :return: Response containing the loan ID and a status of 201 on success. Returns 400 on validation error.
        """
        try:
            self.validator.validate(request.json)
        except ValidationError:
            logger.exception(f"Request body failed validation against JsonSchema")
            return make_response("Invalid request format", 400)

        # Retrieve values from request
        user_id = request.json.get("user_id")
        book_id = request.json.get("book_id")
        due_date = self.generate_due_date()

        # If the library can support this request, do so and persist. Otherwise return.
        loan = Loan(**request.json, due_date=due_date)
        can_borrow, msg = self.can_user_borrow_book(user_id, book_id)
        if can_borrow:
            # Persist
            database.session.add(loan)
            database.session.commit()

            return make_response(str(loan.id), 201)

        return make_response(msg, 400)

    @jwt_required()
    def get(self) -> Response:
        """
        Return all loans in the system.

        :return: Response containing all loans in the system and a status of 200 on success.
        """
        loans = Loan.query.all()
        return make_response(jsonify(loans), 200)
