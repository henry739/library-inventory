from base_test_case import BaseTestCase


class UsersTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.login("senior-librarian-agatha", "books4life")

    def test_create_user_no_json_returns_invalid_status(self):
        rv, status = self.post_json("/users", None)
        self.assertEqual(400, status)

    def test_create_user_empty_json_returns_invalid_status(self):
        rv, status = self.post_json("/users", {})
        self.assertEqual(400, status)

    def test_create_user_with_extra_property_returns_invalid_status(self):
        rv, status = self.post_json("/users", {"full_name": "Alice", "extra": "property"})
        self.assertEqual(400, status)

    def test_create_user_with_id_returns_invalid_status(self):
        rv, status = self.post_json("/users", {"full_name": "Alice", "id": 1})
        self.assertEqual(400, status)

    def test_create_user_with_full_name_succeeds(self):
        rv, status = self.post_json("/users", {"full_name": "Alice"})

        self.assertEqual(201, status)
        self.assertEqual("1", rv)

    def test_created_user_can_be_retrieved_by_id(self):
        resource_id, _ = self.post_json("/users", {"full_name": "Alice"})
        user, status = self.get_by_id("/users", resource_id)

        self.assertEqual(200, status)
        self.assertEqual("Alice", user.get("full_name"))
        self.assertEqual(int(resource_id), user.get("id"))

    def test_get_missing_user_returns_404(self):
        rv, status = self.get_by_id("/users", 100)
        self.assertEqual(404, status)

    def test_multiple_users_can_be_retrieved_by_id(self):
        registrations = self.register_users_by_name(["Alice", "Bob", "Charlie", "David", "Eve"])

        # For each registered user, ensure that the returned object is correct
        for full_name, user_id in registrations.items():
            user, status = self.get_by_id("/users", user_id)

            self.assertEqual(200, status)
            self.assertEqual(user_id, user.get("id"))
            self.assertEqual(full_name, user.get("full_name"))

    def test_users_can_be_searched_for_by_full_name(self):
        registrations = self.register_users_by_name(["Alice", "Bob", "Charlie"])

        for full_name, user_id in registrations.items():
            users, status = self.get_with_params("/users", {"full_name": full_name})

            self.assertEqual(200, status)
            self.assertEqual(1, len(users))
            self.assertEqual(user_id, users[0].get("id"))
            self.assertEqual(full_name, users[0].get("full_name"))

    def test_search_returns_multiple_users_if_they_have_same_full_name(self):
        self.post_json("/users", {"full_name": "Alice"})
        _, creation_status = self.post_json("/users", {"full_name": "Alice"})

        users, search_status = self.get_with_params("/users", {"full_name": "Alice"})

        self.assertEqual(201, creation_status)
        self.assertEqual(200, search_status)
        self.assertEqual(2, len(users))
        self.assertEqual("Alice", users[0].get("full_name"))
        self.assertEqual("Alice", users[1].get("full_name"))
        self.assertNotEqual(users[0].get("id"), users[1].get("id"))

    def test_deletion_of_user_causes_get_by_id_to_return_404(self):
        # Arrange and verify normal state
        user_id, _ = self.post_json("/users", {"full_name": "Alice"})
        _, pre_delete_status = self.get_by_id("/users", user_id)

        # Delete and attempt to retrieve
        deleted_user_id, delete_status = self.delete_by_id("/users", user_id)
        _, post_delete_status = self.get_by_id("/users", user_id)

        # Assert
        self.assertEqual(200, pre_delete_status)
        self.assertEqual(200, delete_status)
        self.assertEqual(404, post_delete_status)
        self.assertEqual(user_id, deleted_user_id)

    def test_deletion_of_missing_resource_returns_404(self):
        rv, status = self.delete_by_id("/users", 100)
        self.assertEqual(404, status)
