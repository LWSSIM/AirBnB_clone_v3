#!/usr/bin/python3
""" Module for the API *states* endpoint """


from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request


@app_views.route('/states', methods=['GET'])
def all_states():
    """ return all states """
    states = storage.all(State)
    states_list = [state.to_dict() for state in states.values()]
    return states_list, 200


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ return a state if exists """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return state.to_dict(), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """ delete state if exists """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return {}, 200


@app_views.route('/states', methods=['POST'])
def post_state():
    """ create a state """
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    elif 'name' not in req:
        abort(400, 'Missing name')

    state = State()
    state.__dict__.update(req)
    state.save()
    return state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """ update a state if exists with all dict keys """
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, 'Not a JSON')

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()
    return state.to_dict(), 200
