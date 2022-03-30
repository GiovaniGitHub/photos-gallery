

from flask import request
from flask_jwt_extended import get_current_user, jwt_required
from flask_restful import Resource
from pexpect import ExceptionPexpect
from project.controllers.album_controller import get_photos_by_album_and_owner
from project.controllers.photo_controller import create_photo
from project.repositories.serialializers import (PhotoRequestSchema,
                                                 PhotoResponseSchema)


class PhotoResource(Resource):
    # @jwt_required()
    # def get(self, album_id):
    #     try:
    #         current_user = get_current_user()
    #         photos = get_photos_by_album_and_owner(album_id=album_id, owner_id=current_user._id)
    #         return PhotoResponseSchema(many=True).dump(photos), 200
    #     except Exception as e:
    #         return e.messages, e.status_code

    @jwt_required()
    def post(self, album_id):
        current_user = get_current_user()
        data = {**dict(request.files), **dict(request.form)}
        photo_data = PhotoRequestSchema().load(data)
        create_photo(user_id=str(current_user.id), album_id=album_id, photo_data=photo_data)

