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
