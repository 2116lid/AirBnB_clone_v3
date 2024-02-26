#!/usr/bin/python3
"""
route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get():
    """
    retrieves all User objects
    """
    user_list = []
    user_obj = storage.all("User")
    for obj in user_obj.values():
        user_list.append(obj.to_dict())

    return jsonify(user_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_route():
    """
    create user route
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    res = jsonify(new_user.to_dict())
    res.status_code = 201

    return res


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    gets a specific User object by ID
    """

    fetch_obj = storage.get("User", str(user_id))

    if fetch_obj is None:
        abort(404)

    return jsonify(fetch_obj.to_dict())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    updates specific User object by ID
    """
    user_json = request.get_json(silent=True)

    if user_json is None:
        abort(400, 'Not a JSON')

    fetch_obj = storage.get("User", str(user_id))

    if fetch_obj is None:
        abort(404)

    for key, val in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetch_obj, key, val)

    fetch_obj.save()

    return jsonify(fetch_obj.to_dict())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete(user_id):
    """
    deletes User by id
    """

    fetch_obj = storage.get("User", str(user_id))

    if fetch_obj is None:
        abort(404)

    storage.delete(fetch_obj)
    storage.save()

    return jsonify({})
