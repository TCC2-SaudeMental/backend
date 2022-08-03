from flask import Flask, g
from flask_cors import CORS
from api.views.auth import auth
from api.views.user import user_b
from api.views.stream import stream_b
from .db import get_engine


def create_app(testing=False):
    app = Flask(__name__)

    CORS(app, origins='*')

    if testing:
        app.config['TESTING'] = True

    @app.before_request
    def create_engine_for_request():
        g.engine = get_engine()

    with app.app_context():

        # Register Blueprints
        app.register_blueprint(auth)
        app.register_blueprint(user_b)
        app.register_blueprint(stream_b)

        return app
