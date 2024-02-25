#!/usr/bin/python3
"""module that contains a JSON response"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


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
def stats_obj():
    """
    stats of all objs route
    """
    data = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for k, v in data.items():
        data[k] = storage.count(v)
    return jsonify(data)
