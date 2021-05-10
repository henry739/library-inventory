from flask import Response, request, make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required

from model.login import Login


class LoginController(Resource):
    def post(self) -> Response:
        username = request.json.get("username")
        password = request.json.get("password")

        login = Login.query.filter(Login.username == username).first()
        if login.password == password:
            token = create_access_token(identity=username)
            return make_response(jsonify(access_token=token), 200)

        return make_response("Incorrect username or password", 401)
