import os
from flask import Flask
from app.routes.book_routes import book_bp
from app.models.database import init_db

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 基礎設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_default_secret_key')
    
    # 註冊 Blueprints
    app.register_blueprint(book_bp)
    
    return app

if __name__ == '__main__':
    # 啟動前先確認並初始化資料庫
    init_db()
    app = create_app()
    app.run(debug=True)
