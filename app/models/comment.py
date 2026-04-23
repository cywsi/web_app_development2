from .database import get_db_connection

class Comment:
    @staticmethod
    def create(book_id, content):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comments (book_id, content) VALUES (?, ?)",
            (book_id, content)
        )
        comment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return comment_id

    @staticmethod
    def get_by_book_id(book_id):
        conn = get_db_connection()
        # 依照時間排序，舊的在上面
        comments = conn.execute(
            "SELECT * FROM comments WHERE book_id = ? ORDER BY created_at ASC", 
            (book_id,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in comments]
        
    @staticmethod
    def delete(comment_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        conn.commit()
        conn.close()
