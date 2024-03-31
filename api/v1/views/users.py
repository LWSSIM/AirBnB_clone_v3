#!/usr/bin/python3
""" Module for the API *users* endpoint """


from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request


@app_views.route('/users', methods=['GET'])
def all_users():
    """ return all users """
    users = storage.all(User)
    users_list = [user.to_dict() for user in users.values()]
    return users_list, 200


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ return a user if exists """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return user.to_dict(), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """ delete user if exists """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route('/users', methods=['POST'])
def post_user():
    """ create a user """
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    elif 'email' not in req:
        abort(400, 'Missing email')
    elif 'password' not in req:
        abort(400, 'Missing password')

    user = User()
    user.__dict__.update(req)
    user.save()
    return user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """ update a user if exists with all dict keys """
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, 'Not a JSON')

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    for key, value in req.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    user.save()
    return user.to_dict(), 200
