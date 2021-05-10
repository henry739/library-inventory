from datetime import datetime, timedelta
from unittest.mock import patch

from base_test_case import BaseTestCase


class LoansTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.login("senior-librarian-agatha", "books4life")

    def test_user_cannot_borrow_book_that_doesnt_exist(self):
        user_id, _ = self.post_json("/users", {"full_name": "Alice"})
        rv, status = self.post_json("/loans", {"user_id": int(user_id), "book_id": 123})

        self.assertEqual(400, status)
        self.assertEqual("Cannot create loan. Book does not exist in the system.", rv)

    def test_non_existent_user_cannot_borrow_book(self):
        book_id, _ = self.post_json("/books", {"title": "1984", "author": "George Orwell"})
        rv, status = self.post_json("/loans", {"user_id": 123, "book_id": int(book_id)})

        self.assertEqual(400, status)
        self.assertEqual("Cannot create loan. User does not exist in the system.", rv)

    def test_user_with_4_loans_cannot_borrow_book(self):
        user_id, _ = self.post_json("/users", {"full_name": "Alice"})
        registered_books = self.register_books_by_title(
            ["1984", "Animal Farm", "Pride and Prejudice", "Harry Potter", "The Lord of the Rings"]
        )

        self.post_json("/loans", {"user_id": int(user_id), "book_id": registered_books["1984"]})
        self.post_json("/loans", {"user_id": int(user_id), "book_id": registered_books["Animal Farm"]})
        self.post_json("/loans", {"user_id": int(user_id), "book_id": registered_books["Pride and Prejudice"]})
        self.post_json("/loans", {"user_id": int(user_id), "book_id": registered_books["Harry Potter"]})

        rv, status = self.post_json(
            "/loans", {"user_id": int(user_id), "book_id": registered_books["The Lord of the Rings"]}
        )

        self.assertEqual(400, status)
        self.assertEqual("Cannot create loan. User has four or more active loans.", rv)

    def test_user_cannot_borrow_book_already_on_loan(self):
        alice_id, _ = self.post_json("/users", {"full_name": "Alice"})
        bob_id, _ = self.post_json("/users", {"full_name": "Bob"})
        book_id, _ = self.post_json("/books", {"title": "1984", "author": "George Orwell"})

        self.post_json("/loans", {"user_id": int(bob_id), "book_id": int(book_id)})
        rv, status = self.post_json(
            "/loans", {"user_id": int(alice_id), "book_id": int(book_id)}
        )

        self.assertEqual(400, status)
        self.assertEqual("Cannot create loan. Book is part of an active loan.", rv)

    def test_user_cannot_borrow_book_if_overdue_on_another_loan(self):
        alice_id, _ = self.post_json("/users", {"full_name": "Alice"})
        n84_id, _ = self.post_json("/books", {"title": "1984", "author": "George Orwell"})
        animal_farm_id, _ = self.post_json("/books", {"title": "Animal Farm", "author": "George Orwell"})

        with patch("api.loans.loans_controller.LoansController.generate_due_date") as m_generate_due_date:
            m_generate_due_date.return_value = datetime.utcnow() - timedelta(1)
            self.post_json("/loans", {"user_id": int(alice_id), "book_id": int(n84_id)})

        rv, status = self.post_json(
            "/loans", {"user_id": int(alice_id), "book_id": int(animal_farm_id)}
        )

        self.assertEqual(400, status)
        self.assertEqual("Cannot create loan. User is overdue on one or more loans.", rv)

    def test_user_can_borrow_book_happy_path(self):
        alice_id, _ = self.post_json("/users", {"full_name": "Alice"})
        n84_id, _ = self.post_json("/books", {"title": "1984", "author": "George Orwell"})

        rv, status = self.post_json(
            "/loans", {"user_id": int(alice_id), "book_id": int(n84_id)}
        )

        self.assertEqual(201, status)

    def test_user_can_return_book(self):
        alice_id, _ = self.post_json("/users", {"full_name": "Alice"})
        n84_id, _ = self.post_json("/books", {"title": "1984", "author": "George Orwell"})
        loan_id, _ = self.post_json("/loans", {"user_id": int(alice_id), "book_id": int(n84_id)})

        rv, status = self.delete_by_id("/loans", int(loan_id))
        _, post_delete_status = self.get_by_id("/loans", int(loan_id))

        self.assertEqual(200, status)
        self.assertEqual(404, post_delete_status)
