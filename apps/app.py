from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_wtf.csrf import CSRFProtect
from apps.config import config


login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.login_message = ""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    login_manager.init_app(app)

    app.logger.setLevel(logging.DEBUG)
    csrf.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    return app
