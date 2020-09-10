#!/usr/bin/python3
"""view for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage as st
from models.user import User


@app_views.route('/users', strict_slashes=False,
                 methods=["GET", "POST"])
@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=["DELETE", "GET", "PUT"])
def get_users(user_id=None):
    """Method to display the welcome text"""
    if user_id:
        user_obj = st.get(Amenity, user_id)
        if user_obj:
            if request.method == "DELETE":
                st.delete(user_obj)
                st.save()
                return jsonify({}), 200
            elif request.method == "GET":
                return jsonify(user_obj.to_dict())
            elif request.method == "PUT":
                data = request.get_json()
                if not data:
                    return jsonify(error="Not a JSON"), 400
                for key, value in data.items():
                    if key not in ["id", "created_at", "updated_at", "email"]:
                        setattr(user_obj, key, value)
                        st.save()
                return jsonify(user_obj.to_dict()), 200
        return abort(404)
    else:
        if request.method == "GET":
            res = st.all('User').values()
            my_list = []
            for user in res:
                my_list.append(user.to_dict())
            return jsonify(my_list)
        elif request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify(error="Not a JSON"), 400
            elif not data.get("email"):
                return jsonify(error="Missing email"), 400
            elif not data.get("password"):
                return jsonify(error="Missing password"), 400
            new_user = User(**data)
            new_user.save()
            return jsonify(new_user.to_dict()), 201
