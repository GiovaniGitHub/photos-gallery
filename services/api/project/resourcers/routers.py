from flask import Blueprint
from flask_restful import Api
from project.repositories.Hello import Helloworld
from project.resourcers.user import LoginResource, UserResource


def init_routes(app):
    bp = Blueprint("restapi", __name__, url_prefix="/api")
    api = Api(bp)

    api.add_resource(Helloworld, "/hello")
    api.add_resource(UserResource, "/users")
    api.add_resource(LoginResource, "/login")
    
    app.register_blueprint(bp)