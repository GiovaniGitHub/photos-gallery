import uuid
from datetime import datetime
from xmlrpc.client import Boolean

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

album_friends = db.Table('album_friends',
    db.Column('albums_id', db.Integer, db.ForeignKey('albums.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
)


class User(db.Model, CRUD):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(256), nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(128), nullable=False)
    comments = db.relationship('comments', backref='users', lazy=True)
    photos = db.relationship("photos", backref='photos', lazy=True)
    albums = db.relationship("albums", backref="albums", lazy=True)
    
    @staticmethod
    def find_by_email(email):
        try:
            user = User.query.field(email=email).get()
            return user
        except db.DoesNotExist:
            return None

    @staticmethod
    def find_by_id(user_id):
        try:
            user = User.query.get(user_id)
            return user
        except db.DoesNotExist:
            return None

    def __init__(self, email, name, password):
        self.name = name
        self.email = email
        self.password = password


class Comment(db.Model, CRUD):
    __tablename__ = "comments"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message = db.Column(String(150), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow())
    updated_at = db.Column(DateTime, default=datetime.utcnow())
    added_by = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    photo = db.Column(UUID(as_uuid=True), db.ForeignKey('photos.id'), nullable=False)


class Photo(db.Model, CRUD):
    __tablename__ = "photos"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(String(60), nullable=False)
    description = db.Column(String(180), nullable=False)
    url = db.Column(String(180), nullable=False)
    likes = db.Column(Integer, default=0)
    approved = db.Column(Boolean, default=False)
    created_at = db.Column(DateTime, default=datetime.utcnow())
    updated_at = db.Column(DateTime, default=datetime.utcnow())
    added_by = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('comments', backref='users', lazy=True)
    album = db.Column(Integer, db.ForeignKey("albums.id"), nullable=False)


class Album(db.Model, CRUD):
    __tablename__ = "albums"
    
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(60), nullable=False)
    created_at = db.DateTimeField(default=datetime.utcnow())
    updated_at = db.DateTimeField(default=datetime.utcnow())
    owner = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    spouse = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    friends = db.relationship("friends", secondary=album_friends)
    photos = db.relationship('photos', backref='photos', lazy=True)
    
    def get_album_by_id(self, id):
        try:
            return Album.query.get(id)
        except db.DoesNotExist:
            return None

    def get_albums_by_owner(self, owner_id):
        try:
            return Album.query.filter(owner=owner_id).all()
        except :
            return None

    def check_user_has_permission(self, user_id):
        if self.owner._id == user_id:
            return True

        if self.spouse._id == user_id:
            return True

        if any(Album.query.filter(Album.friends.any(id=user_id)).all()):
            return True 

        return False

    def get_albums_by_owner(self, owner_id):
        try:
            return Album.query.filter(owner=owner_id).all()
        except db.DoesNotExist:
            return None

    def check_user_is_approver(self, user_id):
        if self.owner.id == user_id:
            return True

        if self.spouse.id == user_id:
            return True

        return False

    def get_approved_photos(self) -> Photo:
        photos = self.photos.filter(approved=True)
        return photos

    def get_approved_photo_by_id(self, photo_id) -> Photo:
        try:
            photo = self.photos.filter(approved=True, id=photo_id).get()
        except db.DoesNotExist:
            return None
        return photo