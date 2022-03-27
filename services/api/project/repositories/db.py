from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    app.config.from_object("project.config.DataBaseConfig")
    db.init_app(app)


def drop_all():
    db.drop_all()


def create_all():
    db.create_all()


def session_commit():
    db.session.commit()
