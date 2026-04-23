import logging
from .database import get_db_connection

logger = logging.getLogger(__name__)

class Comment:
    @staticmethod
    def create(book_id, content):
        """
        為特定的書籍寫入新的留言紀錄
        引數:
          book_id (int): 該篇讀書心得的書籍 ID
          content (str): 使用者輸入的留言內文
        回傳值:
          int: 留言產生的流水號 (ID)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO comments (book_id, content) VALUES (?, ?)",
                (book_id, content)
            )
            comment_id = cursor.lastrowid
            conn.commit()
            return comment_id
        except Exception as e:
            logger.error(f"新增留言失敗: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """
        取得系統內所有的留言記錄
        回傳值:
          list[dict]: 留言記錄清單列表
        """
        try:
            conn = get_db_connection()
            comments = conn.execute("SELECT * FROM comments ORDER BY created_at DESC").fetchall()
            return [dict(row) for row in comments]
        except Exception as e:
            logger.error(f"取得所有留言失敗: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(comment_id):
        """
        利用留言 ID 拿取單條詳細紀錄
        引數:
          comment_id (int): 欲找尋的留言 ID
        回傳值:
          dict: 該留言的詳細資料字典
        """
        try:
            conn = get_db_connection()
            comment = conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,)).fetchone()
            return dict(comment) if comment else None
        except Exception as e:
            logger.error(f"取得單一留言失敗: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_book_id(book_id):
        """
        提取特定書籍文章底下的所有交流回覆，並依發生時間由舊到新排序
        引數:
          book_id (int): 關聯的書籍 ID
        回傳值:
          list[dict]: 按時間遞增排序的留言陣列
        """
        try:
            conn = get_db_connection()
            comments = conn.execute(
                "SELECT * FROM comments WHERE book_id = ? ORDER BY created_at ASC", 
                (book_id,)
            ).fetchall()
            return [dict(row) for row in comments]
        except Exception as e:
            logger.error(f"取得指定書籍留言失敗: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(comment_id, content):
        """
        替換已送出的特定留言內文
        引數:
          comment_id (int): 需要被修改的留言 ID
          content (str): 最新送出的更新文字
        """
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE comments SET content = ? WHERE id = ?",
                (content, comment_id)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"修改留言失敗: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(comment_id):
        """
        清除無用或包含爭議的特定段落
        引數:
          comment_id (int): 欲銷毀的留言 ID
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
            conn.commit()
        except Exception as e:
            logger.error(f"刪除留言失敗: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()
