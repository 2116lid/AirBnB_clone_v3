#!/usr/bin/python3
"""
route for handling Review objects and operations
"""
from models.review import Review
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def review_place(place_id):
    """
    retrieves all review objects by place
    """
    review_list = []
    place_obj = storage.get("Place", str(place_id))

    if place_obj is None:
        abort(404)

    for obj in place_obj.reviews:
        review_list.append(obj.to_dict())

    return jsonify(review_list)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_route(place_id):
    """
    create review route
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", review_json["user_id"]):
        abort(404)
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()
    res = jsonify(new_review.to_dict())
    res.status_code = 201

    return res


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_get(review_id):
    """
    gets a specific Review object by ID
    """

    fetch_obj = storage.get("Review", str(review_id))

    if fetch_obj is None:
        abort(404)

    return jsonify(fetch_obj.to_dict())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """
    updates specific Review object by ID
    """
    place_json = request.get_json(silent=True)

    if place_json is None:
        abort(400, 'Not a JSON')

    fetch_obj = storage.get("Review", str(review_id))

    if fetch_obj is None:
        abort(404)

    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(fetch_obj, key, val)

    fetch_obj.save()

    return jsonify(fetch_obj.to_dict())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete(review_id):
    """
    deletes Review by id
    """

    fetch_obj = storage.get("Review", str(review_id))

    if fetch_obj is None:
        abort(404)

    storage.delete(fetch_obj)
    storage.save()

    return jsonify({})
