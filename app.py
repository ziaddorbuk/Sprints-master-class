from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
import os
username = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')

# Create a PostgreSQL database connection
# db_uri = f'postgresql://{username}:{password}@localhost:5432/bookstore' 
db_uri = f'postgresql://{username}:{password}@postgres:5432/bookstore'
 
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the Book model
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if 'title' in data and 'author' in data:
        new_book = Book(title=data['title'], author=data['author'])
        try:
            session = Session()
            session.add(new_book)
            session.commit()
            return jsonify({'Auther': new_book.author, 'title': new_book.title, 'ID': new_book.id}), 201
        except IntegrityError:
            session.rollback()
            return jsonify({'error': 'Book already exists'}), 400
        finally:
            session.close()
            print('Session closed')
    else:
        return jsonify({'error': 'Invalid book data'}), 400

# Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    try:
        session = Session()
        book = session.query(Book).filter_by(id=book_id).first()
        print(book.author)
        if book:
            if 'title' in data:
                book.title = data['title']
            if 'author' in data:
                book.author = data['author']
            session.commit()
            return jsonify({ 'title': book.title, 'author': book.author}), 200
        else:
            return jsonify({'error': 'Book not found'}), 404
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'Book already exists'}), 400
    finally:
        session.close()
        print('Session closed !')

# Delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        session = Session()
        book = session.query(Book).filter_by(id=book_id).first()
        if book:
            session.delete(book)
            session.commit()
            return jsonify({'message': f'Book with ID {book_id} deleted'}), 200
        else:
            return jsonify({'error': 'Book not found'}), 404
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'IntegrityError'}), 400
    finally:
        session.close()
        print('Session closed')

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    try:
        session = Session()
        books = session.query(Book).all()
        books_data = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
        return jsonify(books_data), 200
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'IntegrityError'}), 400
    finally:
        session.close()
        print('Session closed')

# Get a book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        session = Session()
        book = session.query(Book).filter_by(id=book_id).first()
        if book:
            return jsonify({'id': book.id, 'title': book.title, 'author': book.author}), 200
        else:
            return jsonify({'error': 'Book not found'}), 404
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'IntegrityError'}), 400
    finally:
        session.close()
        print('Session closed')

# Delete all books
@app.route('/books', methods=['DELETE'])
def delete_books():
    try:
        session = Session()
        session.query(Book).delete()
        session.commit()
        return jsonify({'message': 'All books deleted'}), 200
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'IntegrityError'}), 400
    finally:
        session.close()
        print('Session closed')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
