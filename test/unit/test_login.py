from base_test_case import BaseTestCase


class LoginTests(BaseTestCase):
    def test_login_with_user_in_db_should_return_200(self):
        rv, status = self.post_json("/login", {"username": "librarian-barry", "password": "books5life"})
        self.assertEqual(200, status)
        self.assertIn("access_token", rv)

    def test_login_invalid_credentials_should_return_401(self):
        rv, status = self.post_json("/login", {"username": "librarian-barry", "password": "books4life"})
        self.assertEqual(401, status)
        self.assertEqual("Incorrect username or password", rv)
