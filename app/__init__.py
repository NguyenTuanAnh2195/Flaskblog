from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from dotenv import load_dotenv

import os
from config import Config


load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
api = Api()


def register_extensions(app, db = None):
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)


def create_app(test_config: object = None) -> object:
    app = Flask(__name__, instance_relative_config=True)

    if not test_config:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from app.models import User, Post
    from app.auth import auth_bp
    from app.posts import post_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)

    register_extensions(app, db)
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Post': Post
        }
    return app
