#!/usr/bin/python3
"""module that contains a JSON response"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def stat():
    """status of API"""
    return jsonify(status='OK')
