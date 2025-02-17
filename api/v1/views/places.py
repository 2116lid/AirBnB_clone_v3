#!/usr/bin/python3
"""
route for handling Place objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_get(city_id):
    """
    retrieves all Place objects by city
    """
    place_list = []
    city_obj = storage.get("City", str(city_id))

    if city_obj is None:
        abort(404)
    for obj in city_obj.places:
        place_list.append(obj.to_dict())

    return jsonify(place_list)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_route(city_id):
    """
    create place route
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)
    if "user_id" not in place_json:
        abort(400, 'Missing user_id')
    if storage.get("User", place_json["user_id"]) is None:
        abort(404)
    if "name" not in place_json:
        abort(400, 'Missing name')

    place_json["city_id"] = city_id

    new_place = Place(**place_json)
    new_place.save()
    res = jsonify(new_place.to_dict())
    res.status_code = 201

    return res


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """
    gets a specific Place object by ID
    """

    fetch_obj = storage.get("Place", str(place_id))

    if fetch_obj is None:
        abort(404)

    return jsonify(fetch_obj.to_dict())


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    updates specific Place object by ID
    """
    place_json = request.get_json(silent=True)

    if place_json is None:
        abort(400, 'Not a JSON')

    fetch_obj = storage.get("Place", str(place_id))

    if fetch_obj is None:
        abort(404)

    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetch_obj, key, val)

    fetch_obj.save()

    return jsonify(fetch_obj.to_dict())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete(place_id):
    """
    deletes Place by id
    """

    fetch_obj = storage.get("Place", str(place_id))

    if fetch_obj is None:
        abort(404)

    storage.delete(fetch_obj)
    storage.save()

    return jsonify({})
