#!/usr/bin/python3
"""view for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage as st
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=["GET", "POST"])
@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=["DELETE", "GET", "PUT"])
def get_reviews(place_id=None, review_id=None):
    """Method to display the welcome text"""
    if place_id:
        place_obj = st.get(Place, place_id)
        if place_obj:
            if request.method == "GET":
                my_list = []
                for review in place_obj.reviews:
                    my_list.append(review.to_dict())
                return jsonify(my_list)
            elif request.method == "POST":
                data = request.get_json()
                if not data:
                    return jsonify(error="Not a JSON"), 400
                elif not data.get("user_id"):
                    return jsonify(error="Missing user_id"), 400
                elif not data.get("text"):
                    return jsonify(error="Missing text"), 400
                user_obj = st.get(User, data["user_id"])
                if user_obj:
                    data["place_id"] = place_id
                    new_review = Review(**data)
                    new_review.save()
                    return jsonify(new_review.to_dict()), 201
        return abort(404)
    elif review_id:
        review_obj = st.get(Review, review_id)
        if review_obj:
            if request.method == "GET":
                return jsonify(review_obj.to_dict())
            elif request.method == "DELETE":
                st.delete(review_obj)
                st.save()
                return jsonify({}), 200
            elif request.method == "PUT":
                data = request.get_json()
                if not data:
                    return jsonify(error="Not a JSON"), 400
                for key, value in data.items():
                    if key not in ["id", "created_at", "updated_at",
                                   "place_id", "user_id"]:
                        setattr(review_obj, key, value)
                        st.save()
                return jsonify(review_obj.to_dict()), 200
        return abort(404)
