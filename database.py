import sqlite3
from data_model import BookCreate


class BookDataBase:
    def __init__(self):
        self.connection = sqlite3.connect("book.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,
    author TEXT NOT NULL
            )
            """)
        self.connection.commit()

    def create_book(self, book: BookCreate):
        self.cursor.execute(
            """
            INSERT INTO books (title, author) VALUES (?, ?)
            """,
            (book.title, book.author),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_book(self):
        self.cursor.execute("""
            SELECT * FROM books;
            """)
        return self.cursor.fetchall()

    def get_book_withid(self, book_id):
        self.cursor.execute(
            """
            SELECT * FROM books WHERE id = (?) 
            """,
            (book_id,),
        )
        return self.cursor.fetchone()

    def updated_book(self, book_id, title, author):
        self.cursor.execute(
            """
           UPDATE books SET title=? , author = ? WHERE id = ?
            """,
            (title, author, book_id),
        )
        self.connection.commit()
        return self.cursor.rowcount

    def remove_book(self, book_id):
        self.cursor.execute(
            """
            DELETE FROM books WHERE id = (?)
            """,
            (book_id,),
        )
        self.connection.commit()
        return self.cursor.rowcount

    def close_connection(self):
        self.connection.close()
