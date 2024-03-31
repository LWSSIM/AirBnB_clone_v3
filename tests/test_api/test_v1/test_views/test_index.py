#!/usr/bin/python3
'''Test index view'''


import unittest
from api.v1.app import app
import models


class TestIndexView(unittest.TestCase):
    """Test index view api
        Get (url_prefix)/status
    """

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def setUp(self):
        """Set up for testing"""
        self.app = app.test_client()

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_status(self):
        """Test status"""
        with self.app as client:
            response = client.get('/api/v1/status')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'status': 'OK'})

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_stats(self):
        """Test stats"""
        with self.app as client:
            response = client.get('/api/v1/stats')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {
                'amenities': 0,
                'cities': 0,
                'places': 0,
                'reviews': 0,
                'states': 0,
                'users': 0
            })
