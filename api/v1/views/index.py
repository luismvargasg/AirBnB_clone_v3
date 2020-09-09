#!/usr/bin/python3
"""File that routes the status on the object app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Method to display the welcome text"""
    return jsonify(status="OK")
