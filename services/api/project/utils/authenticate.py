from datetime import timedelta

from flask_jwt_extended import JWTManager
from project.repositories.models import User


def init_authentication(app):
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        minutes=int(app.config["TOKEN_EXPIRES"])
    )
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]["id"]
        return User.find_by_id(user_id=identity)
