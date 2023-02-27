import os
from zoneinfo import available_timezones
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Book, Genre, Author, db

#Function to Paginate
ITEMS_PER_PAGE = 10
def paginate(request,selection):
    page = request.args.get('page',1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    books = [book.format() for book in selection]
    current_books = books[start:end]
    return current_books

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)
        CORS(app, resources={r"/api/*": {"origins": "*"}})

    
        
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # ENDPOINTS
    @app.route('/api/books',  methods=["GET"])
    def retrive_all_books():
        books = Book.query.order_by(Book.id).all()
        current_books = paginate(request,books)
        genres = Genre.query.order_by(Genre.genre).all()

        if not books:
            abort(404)
        else:    
            return jsonify({
            'success': True,
            'books': current_books,
            'total_books':len(books),
            'genre': {genre.id: genre.genre for genre in genres},
        })  

    @app.route('/api/authors',  methods=["GET"])
    def retrive_all_authors():
        authors = Author.query.order_by(Author.id).all()  

        if not authors:
            abort(404)
        else:    
            return jsonify({
            'success': True,
            'total_authors':len(authors),
            'authors': {author.id: author.name for author in authors},  
        })

    @app.route('/api/genres',  methods=["GET"])
    def retrive_all_genres():
        genres = Genre.query.order_by(Genre.id).all()
        if not genres:
            abort(404)
        else:    
            return jsonify({
            'success': True,
            'genres': {genre.id: genre.genre for genre in genres}
        })     


    @app.route('/api/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            abort(404)
        else:   
                book.delete()
                return jsonify({
                    'success': True,
                    'deleted': book_id
            }) 
           

    @app.route('/api/books', methods=['POST'])
    def add_book():
        body = request.get_json()

        new_id = body.get('id', None)
        new_name = body.get('name', None)
        new_genre = body.get('genre', None)
        new_author = body.get('author', None)
        new_rating = body.get('rating', None)

        if not new_id or new_name or not new_genre or not new_author or not new_rating:
            abort(400)

        book = Book(new_id,new_name,new_genre,new_author,new_rating)

        try:
            book.insert()

            return jsonify({
                'success': True,
                'created': book.id,
            })

        except:
            abort(422)   


    @app.route('/api/books/search', methods=['POST'])
    def search_books():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term:
            matched_books = Book.query.filter(Book.book.ilike(f"%{search_term}%")).all()
            books = paginate(request, matched_books)

            return jsonify({
                'success': True,
                'books': books,
                'total_books': len(matched_books),
                'current_genre': None
            })
        abort(404) 

    @app.route('/api/genres/<int:id>/books', methods=['GET'])   
    def search_books_by_genre(id):
            genre = Genre.query.filter_by(id=id).one_or_none()
            if genre is None:
                abort(404)
            else:
                books = Book.query.filter_by(genre=genre.id).all()
                books = paginate(request, books)

                return jsonify({
                'success': True,
                'books':books,
                'total_books':len(books),
                'genre': genre.genre,
            })   

    @app.route('/api/authors/<int:id>/books', methods=['GET'])   
    def search_books_by_author(id):
            author = Author.query.filter_by(id=id).one_or_none()
            if author is None:
                abort(404)
            else:
                books = Book.query.filter_by(author=author.id).all()
                books = paginate(request, books)

                return jsonify({
                'success': True,
                'books':books,
                'total_books':len(books),
                'author': author.name,
            })                  

    # ERROR HANDLERS
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app       