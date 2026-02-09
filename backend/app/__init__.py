from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from app.config.settings import Config
from app.utils.error_handler import register_error_handlers
from app.routes.auth import auth_bp
from app.routes.categories import categories_bp
from app.routes.entries import entries_bp
from app.routes.reports import reports_bp


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_object: type[Config] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    import app.models  # noqa: F401

    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(entries_bp, url_prefix="/api/entries")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")

    register_error_handlers(app)
    return app
