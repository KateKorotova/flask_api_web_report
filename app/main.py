from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from app.routes import bp
from app.api import Report, Drivers
from app.models import database as default_database


def create_app(database=None):
    app = Flask(__name__)

    app.register_blueprint(bp)
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    api = Api(app)
    Swagger(app)
    api.add_resource(Report, '/api/v1/report/')
    api.add_resource(Drivers, '/api/v1/drivers/')

    if database is None:
        database = default_database

    database.connect()

    @app.teardown_request
    def teardown_request(exception=None):
        if not database.is_closed():
            database.close()

    return app
