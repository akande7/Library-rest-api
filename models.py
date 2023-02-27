import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from settings import DB_NAME,DB_USER,DB_PASSWORD,DB_HOST

database_path = "postgresql://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre = Column(String)
    author = Column(String)
    rating = Column(Integer)

    def __init__(self, name, genre, author, rating):
        self.name = name
        self.genre = genre
        self.author = author
        self.rating = rating
        

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'genre': self.genre,
            'author': self.author,
            'rating':self.rating
            }

"""
Genre

"""
class Genre(db.Model):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    genre = Column(String)

    def __init__(self, genre):
        self.genre = genre

    def format(self):
        return {
            'id': self.id,
            'genre': self.genre
            }

class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def format(self):
        return {
            'id': self.id,
            'name': self.name
            }