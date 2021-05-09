import logging
from datetime import datetime, timedelta

from flask import jsonify, request, make_response, Response
from flask_restful import Resource
from jsonschema import ValidationError

from database.database import db_session
from model.book import Book
from model.loan import Loan
from model.user import User
from schema.schema_validator import SchemaValidator

logger = logging.Logger(__name__)


class LoansController(Resource):
    """
    Handles requests for checking books in and out
    """
    def __init__(self):
        self._loan_length = 7
        self.validator = SchemaValidator("schema/loan.schema.json")

    def generate_due_date(self):
        now = datetime.utcnow()
        return now + timedelta(self._loan_length)

    def is_loan_possible(self, user_id, book_id):
        user = User.query.filter(User.id == user_id).first()
        book = Book.query.filter(Book.id == book_id).first()

        if user is None or book is None:
            return False

        if len(user.loans) >= 4:
            return False

        now = datetime.utcnow()
        if any(loan.due_date < now for loan in user.loans):
            return False

        if len(book.loans) > 0:
            return False

        # TODO: Handle stale data / race conditions
        return True

    def post(self) -> Response:
        """
        """
        # Validate
        try:
            self.validator.validate(request.json)
            if "id" in request.json:
                return make_response("New records should not contain an ID", 400)

        except ValidationError:
            logger.exception(f"Request body failed validation against JsonSchema")
            return make_response("Invalid request format", 400)

        user_id = request.json.get("user_id")
        book_id = request.json.get("book_id")
        due_date = self.generate_due_date()

        # Ensure the library can support this loan
        loan = Loan(user_id=user_id, book_id=book_id, due_date=due_date)
        if self.is_loan_possible(user_id, book_id):
            # Persist
            db_session.add(loan)
            db_session.commit()

            return make_response(str(loan.id), 201)

        return make_response(f"User {user_id} cannot be loaned {book_id}", 200)

    def get(self) -> Response:
        """
        """
        loans = Loan.query.all()
        return make_response(jsonify(loans), 200)