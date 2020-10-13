"""
Health Insurance Policy API
~~~~~~~~~~~~~~~~~~~~~~~~~

This Module contains all the logic to host a Python Flask Microservice App.
Author: Andrew Davenport

"""

from json import dumps
from flask import Flask, Response
from flask_restplus import Resource
from routes import api
from schemas.models import db

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
api.init_app(app)


# Default Route(s)
@api.route('/healthcheck')
class HealthCheck(Resource):
    """
    A basic endpoint to check if server allocation and endpoints are properly set and running.

    :return: A response with a 200 Status Code and a body of 'OK' if the api is healthy.
    """
    @staticmethod
    def get():
        return Response(dumps('OK'), status=200, mimetype='application/json')


if __name__ == "__main__":
    # Create DB
    with app.app_context():
        db.create_all()
        db.session.commit()

    app.run(debug=True)
