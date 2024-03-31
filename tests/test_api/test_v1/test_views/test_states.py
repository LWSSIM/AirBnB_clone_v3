#!/usr/bin/python3
""" Module for testing states views
    Note:
        * All tests are run from the root directory.
        * Set the environment for db_storage before running the tests:
            [HBNB_ENV=test
            HBNB_MYSQL_USER=hbnb_test
            HBNB_MYSQL_PWD=hbnb_test_pwd
            HBNB_MYSQL_HOST=localhost
            HBNB_MYSQL_DB=hbnb_test_db
            HBNB_TYPE_STORAGE=db]
        * Command to run the test:
            python3 -m unittest discover tests
            or
            python3 -m unittest {path of the test file}
"""


import unittest
from api.v1.app import app
from models import *
from models.state import State


class TestStatesView(unittest.TestCase):
    """Test states view api:
        Get (url_prefix)/states
            (url_prefix)/states/<state_id>

        DELETE (url_prefix)/states/<state_id>

        POST (url_prefix)/states
        with request body:
            "name": "state_name"

        PUT (url_prefix)/states/<state_id>
        with request body:
            "name": "state_name"
    """

    @unittest.skipIf(storage_t != "db", "not testing db storage")
    def setUp(self):
        """Set up for testing"""
        self.app = app.test_client()

    @unittest.skipIf(storage_t != "db", "not testing db storage")
    def test_get_states(self):
        """Test get states"""
        with self.app as client:
            response = client.get('/api/v1/states')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [])

    @unittest.skipIf(storage_t != "db", "not testing db storage")
    def test_get_state(self):
        """Test get state"""
        with self.app as client:
            response = client.get('/api/v1/states/1')
            self.assertEqual(response.status_code, 404)

    @unittest.skipIf(storage_t != "db", "not testing db storage")
    def test_delete_state(self):
        """Test delete state"""
        with self.app as client:
            response = client.delete('/api/v1/states/1')
            self.assertEqual(response.status_code, 404)

    @unittest.skipIf(storage_t != "db", "not testing db storage")
    def test_post_state(self):
        """Test post state"""
        with self.app as client:
            response = client.post('/api/v1/states', json={})
            self.assertEqual(response.status_code, 400)

        with self.app as client:
            response = client.post(
                '/api/v1/states', json={"name": "California"}
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json.get('name'), 'California')
            id = response.json.get('id')
            state = storage.get(State, id)
            storage.delete(state)
            self.assertIsNone(storage.get(State, id))

    @unittest.skipIf(storage_t != "db", "not testing db storage")
    def test_put_state(self):
        """Test put state"""
        id = ""
        with self.app as client:
            response = client.put('/api/v1/states/1', json={})
            self.assertEqual(response.status_code, 404)
        with self.app as client:
            response = client.put(
                '/api/v1/states/1', json={"name": "California"}
                )
            self.assertEqual(response.status_code, 404)
        with self.app as client:
            response = client.post(
                '/api/v1/states', json={"name": "California"}
            )
            self.assertEqual(response.status_code, 201)
            id = response.json.get('id')
        with self.app as client:
            response = client.put(
                f'/api/v1/states/{id}', json={"city": "Santos"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json.get('city'), 'Santos')
        state = storage.get(State, id)
        storage.delete(state)
        self.assertIsNone(storage.get(State, id))
