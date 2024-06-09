# models/Author.py
from database.connection import get_db_connection

class Author:
    def __init__(self, name):
        self._name = name
        self._id = self._create_author()

    def _create_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return author_id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles
            WHERE author_id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines

    def __repr__(self):
        return f'<Author {self._name}>'
