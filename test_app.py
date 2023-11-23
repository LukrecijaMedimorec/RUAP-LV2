# test_app.py

import unittest
from app import app, db, Book

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

    def test_get_book(self):
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

        # Check the content of the response
        self.assertEqual(response.get_json()['message'], 'Book created successfully')

        # Check if the new book is in the database
        with app.app_context():
            new_book = Book.query.filter_by(title='New Book').first()
            self.assertIsNotNone(new_book)

    def test_update_book(self):
        # Add a test book to the database
        with app.app_context():
            book = Book(title='Old Title', author='Old Author')
            db.session.add(book)
            db.session.commit()

        # Data for updating the book
        updated_book_data = {'title': 'New Title', 'author': 'New Author'}

        # Make a request to the API endpoint to update the book
        response = self.app.put('/api/books/1', json=updated_book_data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the content of the response
        self.assertEqual(response.get_json()['message'], 'Book updated successfully')

        # Check if the book in the database has been updated
        with app.app_context():
            updated_book = Book.query.get(1)
            self.assertEqual(updated_book.title, 'New Title')
            self.assertEqual(updated_book.author, 'New Author')

    def test_delete_book(self):
        # Add a test book to the database
        with app.app_context():
            book = Book(title='Book to Delete', author='Author to Delete')
            db.session.add(book)
            db.session.commit()

        # Make a request to the API endpoint to delete the book
        response = self.app.delete('/api/books/1')

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the content of the response
        self.assertEqual(response.get_json()['message'], 'Book deleted successfully')

        # Check if the book has been deleted from the database
        with app.app_context():
            deleted_book = Book.query.get(1)
            self.assertIsNone(deleted_book)

if __name__ == '__main__':
    unittest.main()
