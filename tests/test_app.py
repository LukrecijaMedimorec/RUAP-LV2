# test_app.py

import unittest
from app import app, db  # Import app and db from the app package
from app.models import Book

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Book API Client</h1>', response.data)

    def test_get_all_books(self):
        # Add test data to the database
        with app.app_context():
            book1 = Book(title='Book 1', author='Author 1')
            book2 = Book(title='Book 2', author='Author 2')
            db.session.add_all([book1, book2])
            db.session.commit()

        # Make a request to the API endpoint
        response = self.app.get('/api/books')
        data = response.get_json()

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the content of the response
        self.assertIn('books', data)
        self.assertEqual(len(data['books']), 2)
        self.assertEqual(data['books'][0]['title'], 'Book 1')
        self.assertEqual(data['books'][1]['title'], 'Book 2')

    def test_get_book_by_id(self):
        # Add a test book to the database
        with app.app_context():
            book = Book(title='Test Book', author='Test Author')
            db.session.add(book)
            db.session.commit()

        # Make a request to the API endpoint for the specific book
        response = self.app.get('/api/books/1')
        data = response.get_json()

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the content of the response
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'Test Book')
        self.assertEqual(data['author'], 'Test Author')

    def test_create_book(self):
        # Data for creating a new book
        new_book_data = {'title': 'New Book', 'author': 'New Author'}

        # Make a request to the API endpoint to create a new book
        response = self.app.post('/api/books', json=new_book_data)

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Check if the new book is in the database
        with app.app_context():
            new_book = Book.query.filter_by(title='New Book').first()
            self.assertIsNotNone(new_book)

    # Add more test cases for other endpoints (e.g., test_update_book, test_delete_book)

if __name__ == '__main__':
    unittest.main()
