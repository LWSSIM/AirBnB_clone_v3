#!/usr/bin/python3
""" index to return status of the API """


from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    """ return status of the API """
    return {"status": "OK"}, 200
