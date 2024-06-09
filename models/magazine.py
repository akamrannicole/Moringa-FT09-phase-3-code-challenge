# models/Magazine.py
from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category):
        self._name = name
        self._category = category
        self._id = self._create_magazine()

    def _create_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        conn.commit()
        magazine_id = cursor.lastrowid
        conn.close()
        return magazine_id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and 2 <= len(new_name) <= 16:
            self._name = new_name
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (new_name, self._id))
            conn.commit()
            conn.close()
        else:
            raise ValueError("Name must be a string between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and len(new_category) > 0:
            self._category = new_category
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (new_category, self._id))
            conn.commit()
            conn.close()
        else:
            raise ValueError("Category must be a string longer than 0 characters.")

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles
            WHERE magazine_id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self._id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM articles
            WHERE magazine_id = ?
        ''', (self._id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return authors

    def __repr__(self):
        return f'<Magazine {self._name}>'
