import uuid
from datetime import datetime

from project.repositories.db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

class CRUD():

    def save(self):
        if self.id == None:
            db.session.add(self)
        return db.session.commit()

    def destroy(self):
        db.session.delete(self)
        return db.session.commit()


class User(db.Model, CRUD):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(256), nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(128), nullable=False)
    comments = db.relationship('Comment', backref='users', lazy=True)

    @staticmethod
    def find_by_email(email):
        try:
            user = User.objects(email=email).get()
            return user
        except db.DoesNotExist:
            return None

    @staticmethod
    def find_by_id(user_id):
        try:
            user = User.objects(id=user_id).get()
            return user
        except db.DoesNotExist:
            return None

    def __init__(self, email, name, password):
        self.name = name
        self.email = email
        self.password = password

class Comment(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message = db.Column(String(150), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow())
    updated_at = db.Column(DateTime, default=datetime.utcnow())
    added_by = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)