#!/usr/bin/python3
""" module for places_reviews view """


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """ retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ retrieves a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ deletes a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ creates a Review object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400
    if 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ updates a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    spcl_vals = [
        'id', 'user_id',
        'place_id', 'created_at',
        'updated_at'
    ]
    for key, value in data.items():
        if key not in spcl_vals:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
