#!/usr/bin/python3
"""view for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage as st
from models.state import State


@app_views.route('/states', strict_slashes=False,
                 methods=["GET", "POST"])
@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=["DELETE", "GET", "PUT"])
def get_states(state_id=None):
    """Method to display the welcome text"""
    if state_id:
        state_obj = st.get(State, state_id)
        if state_obj:
            if request.method == "DELETE":
                st.delete(state_obj)
                st.save()
                return jsonify({}), 200
            elif request.method == "GET":
                return jsonify(state_obj.to_dict())
            elif request.method == "PUT":
                data = request.get_json()
                if not data:
                    return jsonify(error="Not a JSON"), 400
                for key, value in data.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        setattr(state_obj, key, value)
                        st.save()
                return jsonify(state_obj.to_dict()), 200
        return abort(404)
    else:
        if request.method == "GET":
            res = st.all('State').values()
            my_list = []
            for state in res:
                my_list.append(state.to_dict())
            return jsonify(my_list)
        elif request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify(error="Not a JSON"), 400
            elif not data.get("name"):
                return jsonify(error="Missing name"), 400
            new_state = State(**data)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
