from marshmallow import Schema, ValidationError, fields, validate, validates

from project.utils.functions import check_file_as_format_valid, get_extension


class UserRequestSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))


class LoginResponseSchema(Schema):
    name = fields.Str(required=True)
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


class PhotoResponseSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    url = fields.URL()
    description = fields.Str()
    likes = fields.Int(dump_default=0)
    approved = fields.Bool(dump_default=False)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class PhotoRequestSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    photo_file = fields.Raw(required=True, type="file")

    @validates("photo_file")
    def validate_photo_file(self, photo_file):
        if get_extension(photo_file.filename) == '':
            raise ValidationError("File without extension in name.")
        if not check_file_as_format_valid(photo_file.filename):
            raise ValidationError("File type not accept.")


class LoginRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AlbumsResponseSchema(Schema):
    id = fields.Str(attribute="_id")
    name = fields.Str(required=True)
    created_at = fields.DateTime()


class CommentRequestSchema(Schema):
    message = fields.Str(required=True)


class CommentResponseSchema(Schema):
    id = fields.Str(required=True)
    message = fields.Str(max_length=150, required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
