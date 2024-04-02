#!/usr/bin/python3
""" Module for the API *cities* endpoint """


from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import abort, jsonify, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def all_cities(state_id):
    """ return all cities in a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities), 200


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ return a city if exists """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return city.to_dict(), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """ delete city if exists """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return {}, 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """ create a city in a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return city.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """ update a city if exists """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return city.to_dict(), 200
