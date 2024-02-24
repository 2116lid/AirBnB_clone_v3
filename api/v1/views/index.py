#!/usr/bin/python3
"""module that contains a JSON response"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def stat():
    """status of API"""
    data = {
        "status": "OK"
    }

    stat = jsonify(data)
    stat.status_code = 200

    return stat


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def status_obj():
    """
    stats of all objs route
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    status_all = jsonify(data)
    status_all.status_code = 200

    return status_all
