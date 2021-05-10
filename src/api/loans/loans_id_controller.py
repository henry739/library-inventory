import logging

from flask import jsonify, make_response, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from model.database import database
from model.loan import Loan

logger = logging.Logger(__name__)


class LoansIdController(Resource):
    """
    Handles requests for managing specific loans
    """

    @jwt_required()
    def get(self, loan_id: int) -> Response:
        """
        Fetch a specific loan record.

        :param loan_id: ID of loan to fetch.
        :return: Response containing the loan object and status of 200, or error message and 404
        """
        loan = Loan.query.filter(Loan.id == loan_id).first()
        if loan is None:
            return make_response("Loan does not exist in the system", 404)

        return make_response(jsonify(loan), 200)

    @jwt_required()
    def delete(self, loan_id: int) -> Response:
        """
        Delete specific loan record. Equivalent to "checking in" a book.

        :param loan_id: ID of loan to delete.
        :return: Response containing the id of deleted loan object, and status of 200, or error message and 404
        """
        loan = Loan.query.filter(Loan.id == loan_id).first()
        if loan is None:
            return make_response("Loan does not exist in the system", 404)

        database.session.delete(loan)
        database.session.commit()

        return make_response(str(loan.id), 200)
