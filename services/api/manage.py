from flask.cli import FlaskGroup
from project import app, db
from project.controllers.user_controller import create_user
from project.repositories.models import User

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session_commit()


@cli.command("seed_db")
def seed_db():
    create_user(User(email="email@email.org", name="John Doo", password = "123456"))


if __name__ == "__main__":
    cli()
