#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_all():
    """
    retrieves all Amenity objects
    """
    new_list = []
    amenity_obj = storage.all("Amenity")
    for obj in amenity_obj.values():
        new_list.append(obj.to_dict())

    return jsonify(new_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_route():
    """
    create amenity route
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    res = jsonify(new_amenity.to_dict())
    res.status_code = 201

    return res


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenityId(amenity_id):
    """
    gets a specific Amenity object by ID
    """

    fetch_obj = storage.get("Amenity", str(amenity_id))

    if fetch_obj is None:
        abort(404)

    return jsonify(fetch_obj.to_dict())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    updates specific Amenity object by ID
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    fetch_obj = storage.get("Amenity", str(amenity_id))
    if fetch_obj is None:
        abort(404)
    for key, val in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetch_obj, key, val)
    fetch_obj.save()
    res = jsonify(fetch_obj.to_dict())
    res.status_code = 200
    return res


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """
    deletes Amenity by id
    """

    fetch_obj = storage.get("Amenity", str(amenity_id))

    if fetch_obj is None:
        abort(404)

    storage.delete(fetch_obj)
    storage.save()

    return jsonify({})
