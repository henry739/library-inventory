import json
from base_test_case import BaseTestCase


class UsersTests(BaseTestCase):
    def test_get_returns_404_if_no_user(self):
        response = self.client.get("/api/v1/users/1")
        self.assertEqual(404, response.status_code)

    def test_get_returns_200_if_user_exists(self):
        # Arrange
        self.client.post("/api/v1/users", data=json.dumps({"full_name": "Alice"}), content_type="application/json")

        # Act & Assert
        response = self.client.get("/api/v1/users/1")
        self.assertEqual(200, response.status_code)

    def test_get_returns_correct_user_when_multiple_users_exist(self):
        # Arrange
        self.client.post(
            "/api/v1/users",
            data=json.dumps({"full_name": "Alice"}),
            content_type="application/json"
        )
        self.client.post(
            "/api/v1/users",
            data=json.dumps({"full_name": "Charlie"}),
            content_type="application/json"
        )
        bob_response = self.client.post(
            "/api/v1/users",
            data=json.dumps({"full_name": "Bob"}),
            content_type="application/json"
        )
        bob_id = bob_response.get_data(as_text=True)

        # Act & Assert
        response = json.loads(self.client.get(f"/api/v1/users/{bob_id}").get_data(as_text=True))
        self.assertEqual("Bob", response.get("full_name"))
