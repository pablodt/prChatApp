from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO, send

# Creación de objeto de SQLAlchemy para la bd
database = SQLAlchemy()
DB_NAME = "database.db"

# Definimos socketIO fuera de cualquier método para utilizarlo en varios
socketIO = None

from .views import views
from .auth import auth
from .models import User


def create_app():
    # Creación de objeto Flask
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "pablo"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'

    database.init_app(app)

    socketIO = SocketIO(app)

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    with app.app_context():
        create_database()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @socketIO.on('message')
    def handle_message(msg):
        print("Message: " + msg)
        send(msg, broadcast=True)

    return app


def create_database():
    if not path.exists("app/instance/" + DB_NAME):
        database.create_all()
        print("Created database")
