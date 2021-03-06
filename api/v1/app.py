#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(self):
    """method that calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """handler for 404 errors that returns a JSON-formatted 404 status
    code response."""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST')
    PORT = getenv('HBNB_API_PORT')
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
