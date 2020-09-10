#!/usr/bin/python3
"""view for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage as st
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=["GET", "POST"])
@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=["DELETE", "GET", "PUT"])
def get_places(place_id=None, city_id=None):
    """Method to display the welcome text"""
    if city_id:
        city_obj = st.get(City, place_id)
        if city_obj:
            if request.method == "GET":
                my_list = []
                for place in city_obj.places:
                    my_list.append(place.to_dict())
                return jsonify(my_list)
            elif request.method == "POST":
                data = request.get_json()
                if not data:
                    return jsonify(error="Not a JSON"), 400
                elif not data.get("user_id"):
                    return jsonify(error="Missing user_id"), 400
                elif not data.get("name"):
                    return jsonify(error="Missing name"), 400
                user_obj = st.get(User, data[user_id])
                if user_obj:
                    data["city_id"] = city_id
                    new_place = Place(**data)
                    new_place.save()
                    return jsonify(new_place.to_dict()), 201
        return abort(404)
    elif place_id:
        place_obj = st.get(Place, place_id)
        if place_obj:
            if request.method == "GET":
                return jsonify(place_obj.to_dict())
            elif request.method == "DELETE":
                st.delete(place_obj)
                st.save()
                return jsonify({}), 200
            elif request.method == "PUT":
                data = request.get_json()
                if not data:
                    return jsonify(error="Not a JSON"), 400
                for key, value in data.items():
                    if key not in ["id", "created_at", "updated_at",
                                   "city_id", "user_id"]:
                        setattr(place_obj, key, value)
                        st.save()
                return jsonify(place_obj.to_dict()), 200
        return abort(404)
