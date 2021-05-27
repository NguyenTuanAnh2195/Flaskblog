from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

import os
from config import Config

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()

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

    db.init_app(app)
    from .models import User, Post
    migrate.init_app(app, db)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Post': Post
        }
    return app
