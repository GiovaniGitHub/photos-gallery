from exceptions import UserAlreadyExists, UserNotFound
from project.repositories.models import User
from project.utils.const import PWD_CONTEXT
from sqlalchemy.exc import IntegrityError

def create_user(name: str, email: str, password: str) -> User:
    user = User(name=name, email=email, password=PWD_CONTEXT.encrypt(password))
    try:
        user.save()
        return user
    except IntegrityError:
        raise UserAlreadyExists(message="User Already Exists")


def login(email: str, password: str):
    user = User.find_by_email(email=email)
    if user and PWD_CONTEXT.verify(password, user.password):
        return user
    return None


def find_user(user_id: str) -> User:
    user = User.find_by_id(user_id)
    if not user:
        raise UserNotFound(message="User Not Found")
    return user
