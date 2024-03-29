#!/usr/bin/python3
""" index to return status of the API """


from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """ return status of the API """
    return {"status": "OK"}, 200


@app_views.route('/stats', methods=['GET'])
def stats():
    """ return stats of the API:
     number of objects by type """
    from models import storage

    return {"amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User"),
            }, 200
