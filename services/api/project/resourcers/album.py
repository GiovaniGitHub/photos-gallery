from flask import request
from flask_jwt_extended import get_current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from project.controllers.album_controller import (add_permission_to_user, create_album,
                                                  get_albums_by_owner)
from project.repositories.serialializers import AlbumsResponseSchema


class AlbumResource(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_current_user()
            album_data = request.get_json()
            create_album(owner_id=current_user.id, album_title=album_data['name'])
            return None, 201
        except ValidationError as e:
            return e.messages, e.status_code
    
    @jwt_required()
    def get(self):
        try:
            current_user = get_current_user()
            albums = get_albums_by_owner(owner_id=str(current_user.id))
            return AlbumsResponseSchema(many=True).dump(albums), 200
        except ValidationError as e:
            return e.messages, e.status_code

class FriendAlbumResource(Resource):
    @jwt_required()
    def put(self, album_id, user_email):
        current_user = get_current_user()
        album_data = request.get_json()
        add_permission_to_user(album_id, user_email, current_user.id)