#!/usr/bin/python3
""" Module for the API *places* endpoint """


from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import request, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return places, 200


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return place.to_dict(), 200


@app_views.route('/places/<place_id>', methods=['DELETE'])
def del_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """ Creates a Place object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')

    if storage.get(User, data['user_id']) is None:
        abort(404) # User not found

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return place.to_dict(), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return place.to_dict(), 200