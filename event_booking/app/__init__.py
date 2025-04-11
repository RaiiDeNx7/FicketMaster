from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)

    from .routes import main
    from .api import api

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')

    return app
