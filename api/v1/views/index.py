#!/usr/bin/python3
"""module that contains a JSON response"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False))
def stat():
    """status of API"""
    data = {
        "status": "OK"
    }

    stat = jsonify(data)
    stat.status_code = 200

    return stat
