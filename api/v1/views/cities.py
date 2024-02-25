#!/usr/bin/python3
"""route for handling city object"""
from models.city import City
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_state(state_id):
    """
    retrieves all City objects from a specific state
    """
    city_list = []
    state_obj = storage.get("State", state_id)

    if state_obj is None:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_dict())

    return jsonify(city_list)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_route(state_id):
    """
    create city route
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    res = jsonify(new_city.to_dict())
    res.status_code = 201

    return res


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """
    gets a specific City object by ID
    """

    fetch_obj = storage.get("City", str(city_id))

    if fetch_obj is None:
        abort(404)

    return jsonify(fetch_obj.to_dict())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    updates specific City object by ID
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    fetch_obj = storage.get("City", str(city_id))
    if fetch_obj is None:
        abort(404)
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetch_obj, key, val)
    fetch_obj.save()
    return jsonify(fetch_obj.to_dict())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete(city_id):
    """
    deletes City by id
    """

    fetch_obj = storage.get("City", str(city_id))

    if fetch_obj is None:
        abort(404)

    storage.delete(fetch_obj)
    storage.save()

    return jsonify({})
