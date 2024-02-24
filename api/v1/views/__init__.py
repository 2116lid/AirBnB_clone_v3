#!/usr/bin/python3
"""module for constructing and extending the app"""
from flask import Blueprint


app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")


from api.v1.views.index import *
