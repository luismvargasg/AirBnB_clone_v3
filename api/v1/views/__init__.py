#!usr/bin/python3
"""init file to connect the blueprints"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


if (__name__ == 'api.v1.views'):
    from api.v1.views.index import *
    from api.v1.views.states import *