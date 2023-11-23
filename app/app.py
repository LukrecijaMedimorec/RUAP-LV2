# app.py

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/books', methods=['GET'])
def get_all_books():
    # Replace with your actual API URL
    api_url = 'http://localhost:5000/api/books'
    response = requests.get(api_url)
    books = response.json()['books']
    return jsonify({'books': books})

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Replace with your actual API URL
    api_url = f'http://localhost:5000/api/books/{book_id}'
    response = requests.get(api_url)
    book = response.json()
    return jsonify(book)

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    # Replace with your actual API URL
    api_url = 'http://localhost:5000/api/books'
    response = requests.post(api_url, json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
