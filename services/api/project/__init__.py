from flask import Flask

from exceptions import handle_api_exceptions
from project.repositories import db
from project.resourcers.routers import init_routes
from project.utils.authenticate import init_authentication

app = Flask(__name__)
app.config.from_object("project.config.BaseConfig")
init_authentication(app)
db.init_db(app)
init_routes(app)
handle_api_exceptions(app)
