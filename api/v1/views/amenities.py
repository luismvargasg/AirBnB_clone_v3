#!/usr/bin/python3
"""view for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage as st
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,
                 methods=["GET", "POST"])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["DELETE", "GET", "PUT"])
def get_amenities(amenity_id=None):
    """Method to display the welcome text"""
    if amenity_id:
        amenity_obj = st.get(Amenity, amenity_id)
        if amenity_obj:
            if request.method == "DELETE":
                st.delete(amenity_obj)
                st.save()
                return jsonify({}), 200
            elif request.method == "GET":
                return jsonify(amenity_obj.to_dict())
            elif request.method == "PUT":
                data = request.get_json()
                if not data:
                    return jsonify(error="Not a JSON"), 400
                for key, value in data.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        setattr(amenity_obj, key, value)
                        st.save()
                return jsonify(amenity_obj.to_dict()), 200
        return abort(404)
    else:
        if request.method == "GET":
            res = st.all('Amenity').values()
            my_list = []
            for amenity in res:
                my_list.append(amenity.to_dict())
            return jsonify(my_list)
        elif request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify(error="Not a JSON"), 400
            elif not data.get("name"):
                return jsonify(error="Missing name"), 400
            new_amenity = Amenity(**data)
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201
