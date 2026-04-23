import sqlite3
import os

# 預設 SQLite 資料庫檔案存放於 instance 資料夾內
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得 SQLite 資料庫連線，並設定為字典模式"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 讓查詢結果能以類似字典 (dict) 方式存取欄位 (例: row['title'])
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    """初始化資料庫，讀取 schema.sql 並建表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if not os.path.exists(schema_path):
        return
        
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()

    conn = get_db_connection()
    conn.executescript(schema)
    conn.commit()
    conn.close()
