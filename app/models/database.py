import sqlite3
import os
import logging

# 設定基礎 Log，便於觀察資料庫錯誤
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """
    取得關聯式資料庫 SQLite 的連線對象
    回傳值: SQLite 連線物件 (連線已附帶 sqlite3.Row 以便採用字典的方式讀取欄位)
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  
        return conn
    except Exception as e:
        logger.error(f"資料庫連線失敗: {e}")
        raise

def init_db():
    """
    初始化資料庫。
    這將讀取專案底下的 `database/schema.sql` 檔案並予以執行，
    建立不存在的表格及其資料欄位。
    """
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if not os.path.exists(schema_path):
        logger.warning(f"找不到建表 SQL 腳本: {schema_path}")
        return
        
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()

        conn = get_db_connection()
        conn.executescript(schema)
        conn.commit()
        conn.close()
        logger.info("資料庫初始化完成")
    except Exception as e:
        logger.error(f"初始化資料庫失敗: {e}")
