#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_state():
    """
    retrieves all State objects
    """
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_dict())

    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_route():
    """
    create state route
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    res = jsonify(new_state.to_dict())
    res.status_code = 201

    return res


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    gets a specific State object by ID
    """

    fetch_obj = storage.get("State", str(state_id))

    if fetch_obj is None:
        abort(404)

    return jsonify(fetch_obj.to_dict())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    updates specific State object by ID
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetch_obj = storage.get("State", str(state_id))
    if fetch_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetch_obj, key, val)
    fetch_obj.save()
    return jsonify(fetch_obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    """
    deletes State by id
    """

    fetch_obj = storage.get("State", str(state_id))

    if fetch_obj is None:
        abort(404)

    storage.delete(fetch_obj)
    storage.save()

    return jsonify({})
