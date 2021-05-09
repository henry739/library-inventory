from flask import Flask, make_response
from flask_restful import Api, Resource

API_BASE = "/api/v1"


class TestResource(Resource):
    def get(self):
        return make_response("Hello World!", 200)


if __name__ == "__main__":
    server = Flask(__name__)
    api = Api(server)

    api.add_resource(TestResource, "/")

    server.run()
