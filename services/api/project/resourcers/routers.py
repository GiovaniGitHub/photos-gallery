from flask import Blueprint
from flask_restful import Api

from project.resourcers import Alive
from project.resourcers.album import AlbumResource, FriendAlbumResource
from project.resourcers.photo import PhotoResource
from project.resourcers.user import LoginResource, UserResource


def init_routes(app):
    bp = Blueprint("restapi", __name__, url_prefix="/api")
    api = Api(bp)

    api.add_resource(Alive, "/hello")
    api.add_resource(UserResource, "/users")
    api.add_resource(LoginResource, "/login")
    
    api.add_resource(AlbumResource, "/albums")
    api.add_resource(FriendAlbumResource, "/album/<string:album_id>/friend/<string:user_email>")
    # api.add_resource(PhotoResource, "/album/<string:album_id>/photos")
    
    app.register_blueprint(bp)