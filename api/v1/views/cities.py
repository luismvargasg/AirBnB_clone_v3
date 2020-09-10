#!/usr/bin/python3
"""view for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage as st
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=["GET", "POST"])
@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=["DELETE", "GET", "PUT"])
def get_cities(state_id=None, city_id=None):
    """Method to display the welcome text"""
    if state_id:
        state_obj = st.get(State, state_id)
        if state_obj:
            if request.method == "GET":
                my_list = []
                for city in state_obj.cities:
                    my_list.append(city.to_dict())
                return jsonify(my_list)
            elif request.method == "POST":
                data = request.get_json()
                if not data:
                    return jsonify(error="Not a JSON"), 400
                elif not data.get("name"):
                    return jsonify(error="Missing name"), 400
                data["state_id"] = state_id
                new_city = City(**data)
                new_city.save()
                return jsonify(new_city.to_dict()), 201
        return abort(404)
    elif city_id:
        city_obj = st.get(City, city_id)
        if city_obj:
            if request.method == "GET":
                return jsonify(city_obj.to_dict())
            elif request.method == "DELETE":
                st.delete(city_obj)
                st.save()
                return jsonify({}), 200
            elif request.method == "PUT":
                data = request.get_json()
                if not data:
                    return jsonify(error="Not a JSON"), 400
                for key, value in data.items():
                    if key not in ["id", "created_at", "updated_at",
                                   "state_id"]:
                        setattr(city_obj, key, value)
                        st.save()
                return jsonify(city_obj.to_dict()), 200
        return abort(404)
