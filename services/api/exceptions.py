from flask.json import jsonify


class BaseException(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        data = dict(self.payload or ())
        data["message"] = self.message
        data["status_code"] = self.status_code
        return data


class UserNotFound(BaseException):
    status_code = 404


class FileUploadException(BaseException):
    status_code = 400


class UserAlreadyExists(BaseException):
    status_code = 400


class LoginUnauthorized(BaseException):
    status_code = 401


class AlbumNotFound(BaseException):
    status_code = 404


class UnauthorizedPhotoUpdate(BaseException):
    status_code = 401


class UnauthorizedPhotoComment(BaseException):
    status_code = 401


class AlbumCreateException(BaseException):
    status_code = 400


class PhotoNotFound(BaseException):
    status_code = 404


class AlbumPermission(BaseException):
    status_code = 401


def handle_api_exceptions(app):
    @app.errorhandler(UserNotFound)
    def handle_user_not_found(e):
        return jsonify(e.to_dict())

    @app.errorhandler(LoginUnauthorized)
    def handle_login_unauthorized(e):
        return jsonify(e.to_dict())

    @app.errorhandler(AlbumNotFound)
    def handle_album_not_found(e):
        return jsonify(e.to_dict())

    @app.errorhandler(AlbumPermission)
    def handle_album_permission_denied(e):
        return jsonify(e.to_dict())

    @app.errorhandler(FileUploadException)
    def handle_file_upload_error(e):
        return jsonify(e.to_dict())

    @app.errorhandler(PhotoNotFound)
    def handle_photo_not_found_error(e):
        return jsonify(e.to_dict())

    @app.errorhandler(UnauthorizedPhotoComment)
    def handle_photo_comment_unauthorized(e):
        return jsonify(e.to_dict())
