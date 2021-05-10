from base_test_case import BaseTestCase


class BooksTests(BaseTestCase):
    def test_librarian_cannot_add_book(self):
        self.login("librarian-barry", "books5life")
        _, create_status = self.post_json("/books", {"title": "1984", "author": "George Orwell"})
        books, _ = self.get_with_params("/books", {"title": "1984"})

        self.assertEqual(403, create_status)
        self.assertEqual(0, len(books))

    def test_librarian_cannot_delete_book(self):
        self.login("senior-librarian-agatha", "books4life")
        n84_id, _ = self.post_json("/books", {"title": "1984", "author": "George Orwell"})

        self.login("librarian-barry", "books5life")
        _, delete_status = self.delete_by_id("/books", n84_id)
        books, _ = self.get_with_params("/books", {"title": "1984"})

        self.assertEqual(403, delete_status)
        self.assertEqual(1, len(books))

    def test_senior_librarian_can_add_book(self):
        self.login("senior-librarian-agatha", "books4life")
        n84_id, create_status = self.post_json("/books", {"title": "1984", "author": "George Orwell"})
        book, _ = self.get_by_id("/books", int(n84_id))

        self.assertEqual(201, create_status)
        self.assertEqual("1984", book.get("title"))

    def test_senior_librarian_can_delete_book(self):
        self.login("senior-librarian-agatha", "books4life")
        n84_id, _ = self.post_json("/books", {"title": "1984", "author": "George Orwell"})
        _, delete_status = self.delete_by_id("/books", n84_id)
        books, _ = self.get_with_params("/books", {"title": "1984"})

        self.assertEqual(200, delete_status)
        self.assertEqual(0, len(books))
