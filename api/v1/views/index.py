#!/usr/bin/python3
"""File that routes the status on the object app_views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage as st


@app_views.route('/status', strict_slashes=False)
def status():
    """Method to display the welcome text"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Method that retrieves the number of each object by type"""
    return jsonify(amenities=st.count('Amenity'),
                   cities=st.count('City'),
                   places=st.count('Place'),
                   reviews=st.count('Review'),
                   states=st.count('State'),
                   users=st.count('User'))
