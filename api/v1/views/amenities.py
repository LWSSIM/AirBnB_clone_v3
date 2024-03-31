#!/usr/bin/python3
""" holds views for Amenity objects"""


from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, request


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """ return all amenities """
    amenities = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()]
    return amenities_list, 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ return amenity if exists """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return amenity.to_dict(), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity if exists """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """ create an amenity """
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    elif 'name' not in req:
        abort(400, 'Missing name')

    amenity = Amenity()
    amenity.__dict__.update(req)
    amenity.save()
    return amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """ update an amenity if exists with all dict keys """
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, 'Not a JSON')

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    amenity.save()
    return amenity.to_dict(), 200
