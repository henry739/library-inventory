from flask import Response, request, make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity

from model.login import Login


class LoginController(Resource):
    SENIOR_ROLE = "senior"

    @staticmethod
    def senior_authorization_required(endpoint_function):
        def authorization_wrapper(*args, **kwargs):
            username = get_jwt_identity()
            authenticated_user = Login.query.filter(Login.username == username).first()

            if authenticated_user.role == LoginController.SENIOR_ROLE:
                return endpoint_function(*args, **kwargs)

            return make_response("Unauthorized", 403)
        return authorization_wrapper

    def post(self) -> Response:
        username = request.json.get("username")
        password = request.json.get("password")

        login = Login.query.filter(Login.username == username).first()
        if login.password == password:
            token = create_access_token(identity=username)
            return make_response(jsonify(access_token=token), 200)

        return make_response("Incorrect username or password", 401)
