# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)

@app.route('/api/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
    return jsonify({'books': book_list})

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author})
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        data = request.get_json()
        book.title = data['title']
        book.author = data['author']
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    else:
        return jsonify({'message': 'Book not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
