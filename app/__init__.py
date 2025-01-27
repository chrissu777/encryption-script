from flask import Flask
from .routes import upload_bp


def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile('config.py')
    app.register_blueprint(upload_bp)

    return app
