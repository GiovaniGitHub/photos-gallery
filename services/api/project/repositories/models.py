import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String

from project.repositories.db import db


class CRUD():
    def save(self):
        db.session.add(self)
        return db.session.commit()

    def destroy(self):
        db.session.delete(self)
        return db.session.commit()


album_friends = db.Table('album_friends',
    db.Column('albums_id', db.Integer, db.ForeignKey('albums.id', ondelete="CASCADE")),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
)


class User(db.Model, CRUD):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(256), nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(128), nullable=False)
    
    @staticmethod
    def find_by_email(email):
        try:
            user = User.query.filter(User.email==email).one()
            return user
        except NoResultFound:
            return None

    @staticmethod
    def find_by_id(user_id):
        try:
            user = User.query.get(user_id)
            return user
        except NoResultFound:
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
    added_by_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    photo_id = db.Column(UUID(as_uuid=True), db.ForeignKey('photos.id'), nullable=False)

    db.relationship("User", foreign_keys=[added_by_id])
    db.relationship("Photo", foreign_keys=[photo_id])

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
    added_by_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    album_id = db.Column(Integer, db.ForeignKey("albums.id"), nullable=False)
    
    added_by = db.relationship("User", foreign_keys=[added_by_id])
    album = db.relationship("Album", foreign_keys=[album_id])


class Album(db.Model, CRUD):
    __tablename__ = "albums"
    
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(60), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow())
    updated_at = db.Column(DateTime, default=datetime.utcnow())
    owner_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    spouse_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=True)
    friends = db.relationship("User", secondary=album_friends)
    photos = db.relationship('Photo', backref='photos', lazy=True, cascade="all, delete")
    
    owner = db.relationship("User", foreign_keys=[owner_id])
    spouse = db.relationship("User", foreign_keys=[spouse_id])

    @staticmethod
    def get_album_by_id(id):
        try:
            return Album.query.get(id)
        except NoResultFound as e:
            print(e)
            return None

    @staticmethod
    def get_albums_by_owner(owner_id):
        try:
            return Album.query.filter(Album.owner_id==owner_id).all()
        except NoResultFound:
            return None

    @staticmethod
    def get_album_by_id_and_owner(id, owner_id):
        try:
            return Album.query.filter(Album.id==id, Album.owner_id==owner_id).one()
        except NoResultFound:
            return None
        
    def check_user_has_permission(self, user_id):

        if self.owner_id == int(user_id):
            return True

        if self.spouse_id == int(user_id):
            return True

        if any(Album.query.filter(Album.friends.any(id=user_id)).all()):
            return True 

        return False

    def get_albums_by_owner(self, owner_id):
        try:
            return Album.query.filter(Album.owner_id==owner_id).all()
        except NoResultFound:
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
        except Exception as e:
            print(e)
            return None
        return photo
    
    def add_friend(self, email):
        try:
            user = User.find_by_email(email)
            self.friends.append(user)
            self.save()
        except Exception as e:
            print(e)
            return False
        return True

    def add_photo(self, photo):
        try:
            self.photos.append(photo)
            self.save()
        except Exception as e:
            print(e)
            return False
        return True