import os
import unittest

os.environ["DB_NAME"] = "test_library.db"

from app import app, init_db


class LibraryAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret"
        init_db()
        self.client = app.test_client()

    def test_register_and_login(self):
        register_response = self.client.post(
            "/register",
            data={"username": "demo", "email": "demo@example.com", "password": "secret123"},
            follow_redirects=True,
        )
        self.assertIn(b"Please log in", register_response.data)

        login_response = self.client.post(
            "/login",
            data={"username": "demo", "password": "secret123"},
            follow_redirects=True,
        )
        self.assertIn(b"Dashboard", login_response.data)


if __name__ == "__main__":
    unittest.main()
