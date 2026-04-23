from .database import get_db_connection

class Book:
    @staticmethod
    def create(title, review, rating):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, review, rating) VALUES (?, ?, ?)",
            (title, review, rating)
        )
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return book_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        books = conn.execute("SELECT * FROM books ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(row) for row in books]

    @staticmethod
    def get_by_id(book_id):
        conn = get_db_connection()
        book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        conn.close()
        return dict(book) if book else None

    @staticmethod
    def search_by_title(keyword):
        conn = get_db_connection()
        # 使用 LIKE 進行模糊搜尋，前後加上 %
        books = conn.execute(
            "SELECT * FROM books WHERE title LIKE ? ORDER BY created_at DESC", 
            (f'%{keyword}%',)
        ).fetchall()
        conn.close()
        return [dict(row) for row in books]
        
    @staticmethod
    def delete(book_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
