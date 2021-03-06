from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required)
from flask_restful import Resource
from marshmallow import ValidationError

from exceptions import AlbumNotFound, LoginUnauthorized, UserAlreadyExists
from project.controllers.album_controller import get_albums_by_owner
from project.controllers.user_controller import create_user, login
from project.repositories.serialializers import (AlbumsResponseSchema,
                                                 LoginRequestSchema,
                                                 LoginResponseSchema,
                                                 UserRequestSchema,
                                                 UserResponseSchema)


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            data = LoginRequestSchema().load(request.get_json())
            user = login(**data)
            if user:
                info = {"email": user.email, "id": str(user.id)}
                data_login = LoginResponseSchema().dump({
                    "name": user.name,
                    "access_token": create_access_token(info),
                    "refresh_token": create_refresh_token(info)})
                return data_login, 200

        except ValidationError as e:
            return e.messages, 400
        except LoginUnauthorized as e:
            return e.message, 400


class UserResource(Resource):
    def post(self):
        try:
            data = UserRequestSchema().load(request.get_json())
            user = create_user(**data)
            return UserResponseSchema().dump(user), 200

        except ValidationError as e:
            return e.messages, 400
        except UserAlreadyExists as e:
            return e.to_dict(), e.status_code


class UserAlbumsResource(Resource):
    @jwt_required()
    def get(self, owner_id):
        try:
            albums = get_albums_by_owner(owner_id)
            return AlbumsResponseSchema(many=True).dump(albums), 200
        except AlbumNotFound as e:
            return e.to_dict(), e.status_code
