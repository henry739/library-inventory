import logging

from flask import jsonify, make_response, Response
from flask_restful import Resource

from database.database import db_session
from model.loan import Loan

logger = logging.Logger(__name__)


class LoansIdController(Resource):
    """
    Handles requests for managing specific loans
    """

    def get(self, loan_id: int) -> Response:
        """

        :param loan_id:
        :return:
        """
        loan = Loan.query.filter(Loan.id == loan_id).first()
        if loan is None:
            return make_response("Loan does not exist in the system", 404)

        return make_response(jsonify(loan), 200)

    def delete(self, loan_id: int) -> Response:
        """

        :param loan_id:
        :return:
        """
        loan = Loan.query.filter(Loan.id == loan_id).first()
        if loan is None:
            return make_response("Loan does not exist in the system", 404)

        db_session.delete(loan)
        db_session.commit()

        return make_response(str(loan.id), 200)
