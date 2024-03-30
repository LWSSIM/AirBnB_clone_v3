#!/usr/bin/python3
""" Module for the API first endpoint """


from flask import Flask
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')


@app.errorhandler(404)
def page_not_found(e):
    """ Method to handle 404 error """
    return {"error": "Not found"}, 404


@app.teardown_appcontext
def teardown(self):
    """ Method to close the session """
    from models import storage

    storage.close()


if __name__ == "__main__":
    if host is None and port is None:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    else:
        app.run(host=host, port=port, threaded=True)
