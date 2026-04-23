import logging
from .database import get_db_connection

logger = logging.getLogger(__name__)

class Book:
    @staticmethod
    def create(title, review, rating):
        """
        新增一筆書籍心得記錄
        引數:
          title (str): 書籍名稱
          review (str): 心得內容
          rating (int): 給予書籍的分數 (1-5)
        回傳值:
          int: 新建立資料的 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (title, review, rating) VALUES (?, ?, ?)",
                (title, review, rating)
            )
            book_id = cursor.lastrowid
            conn.commit()
            return book_id
        except Exception as e:
            logger.error(f"新增書籍失敗: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有筆記清單，按照最後建立的時間排序
        回傳值:
          list[dict]: 包含所有書籍心得紀錄的 list
        """
        try:
            conn = get_db_connection()
            books = conn.execute("SELECT * FROM books ORDER BY created_at DESC").fetchall()
            return [dict(row) for row in books]
        except Exception as e:
            logger.error(f"取得所有書籍失敗: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(book_id):
        """
        依據書籍 ID 取得特定的書籍心得紀錄
        引數:
          book_id (int): 欲查詢的書籍 ID
        回傳值:
          dict: 書籍紀錄字典，若無此書則回傳 None
        """
        try:
            conn = get_db_connection()
            book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
            return dict(book) if book else None
        except Exception as e:
            logger.error(f"取得單一書籍失敗: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(book_id, title, review, rating):
        """
        更新特定書籍內容
        引數:
          book_id (int): 要更新的書籍 ID
          title (str): 新的書名
          review (str): 新的心得
          rating (int): 新的分數
        """
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE books SET title = ?, review = ?, rating = ? WHERE id = ?",
                (title, review, rating, book_id)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"更新書籍失敗: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(book_id):
        """
        刪除一個特定書籍紀錄與心得。若開啟外鍵 Cascade 功能，底下的相關留言將一併清除。
        引數:
          book_id (int): 要刪除的書籍 ID
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
        except Exception as e:
            logger.error(f"刪除書籍失敗: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def search_by_title(keyword):
        """
        給定關鍵字，透過模糊搜尋找到合適的書名
        引數:
          keyword (str): 要查詢的關鍵字
        回傳值:
          list[dict]: 符合條件的紀錄 list
        """
        try:
            conn = get_db_connection()
            books = conn.execute(
                "SELECT * FROM books WHERE title LIKE ? ORDER BY created_at DESC", 
                (f'%{keyword}%',)
            ).fetchall()
            return [dict(row) for row in books]
        except Exception as e:
            logger.error(f"搜尋書籍失敗: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
