import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from auth.auth import AuthError


class TestSecureAPI(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_drinks(self):
        result = self.client().get('/drinks')
        self.assertEqual(result.status_code, 200)

    def test_get_drink_details(self):

        headers = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNIWnB1RGkzOXFfVkRsM1M1ZEltXyJ9.eyJpc3MiOiJodHRwczovL2JsdWIuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODc0ZDU0ODVkZDk4MGM2OGQ5MjViMyIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTU4NjEwNzQ2NCwiZXhwIjoxNTg2MTE0NjY0LCJhenAiOiJNZU9ZWlhob0hjSDI5Uzg0MUcxVGZYNDlrbnJmNkF0SiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.X2xz0QaLo6UpitX63P4sqaz0bQ5MS7_b74OI25JWIePg9xzzWwi_fZoGkWe9sAfIsj8rLLrMFuvtxpCVKhiKGIt-z0Ccf6zBa6KuJpUP9LhZEOt8mGMCrhC3uchpV5KyJgQ9co_zncm-UPjoO4_GT1tMfZHxR-PKeCbd7Ch7r5eE98b0mabRDrTevJnfEPTsVShLlvCWPsoPM2hf_8PInC1Wo1u0SfCtzifP28-p5sH_qBhDuFb2f-RPiIJLQ6xbKu_GC5-r8uAK8XQG0Jwjc5nw3Htpt4Kkdtfe8UEOlmHcaHizKLnFGBYs_GbjqLW8Pv6qLsqhOo1-NWNXqisRGg",
            "Content-Type": "application/json"
        }

        result = self.client().get('/drinks-detail', headers=headers)
        self.assertEqual(result.status_code, 200)

    def test_get_drink_details_without_rights(self):
        self.assertRaises(Exception, self.client().get, '/drinks-detail')


        # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
