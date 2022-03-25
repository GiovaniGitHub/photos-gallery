from flask import request
from exceptions import AlbumNotFound, LoginUnauthorized, UserAlreadyExists
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required)
from flask_restful import Resource
from marshmallow import ValidationError
from project.controllers.user_controller import create_user, get_albums_by_owner, login
from project.repositories.serialializers import AlbumsResponseSchema, LoginRequestSchema, LoginResponseSchema, UserRequestSchema


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            data = LoginRequestSchema().load(request.get_json())
            user = login(**data)
            if user:
                info = {"email": user.email, "id": str(user._id)}
                data_login = LoginResponseSchema().dump({
                    "name": user.name,
                    "access_token": create_access_token(info),
                    "refresh_token": create_refresh_token(info)})
                return data_login, 200

        except ValidationError as e:
            print("Entrou no primeiro")
            return e.to_dict(), 400
        except LoginUnauthorized as e:
            print("Entrou no segundo")
            return e.to_dict(), 400


class UserResource(Resource):
    def post(self):
        try:
            data = UserRequestSchema().load(request.get_json())
            create_user(**data)
            return None, 200

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
