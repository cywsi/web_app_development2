from flask import Blueprint, render_template, request, redirect, url_for, flash

book_bp = Blueprint('book_routes', __name__)

@book_bp.route('/')
def index():
    """
    HTTP GET: 首頁 (列出所有書籍心得)
    輸入: 無
    處理邏輯: 呼叫 Book.get_all() 取得書籍清單
    輸出: 渲染 templates/index.html
    """
    pass

@book_bp.route('/search')
def search():
    """
    HTTP GET: 搜尋書籍
    輸入: Query string `q`
    處理邏輯: 若有 q，呼叫 Book.search_by_title(q)，否則回到預設全清單
    輸出: 將搜尋結果帶入 templates/index.html 進行渲染
    """
    pass

@book_bp.route('/books/new', methods=['GET', 'POST'])
def create():
    """
    HTTP GET: 顯示新增書籍表單
    HTTP POST: 處理新增書籍邏輯
    輸入: Form data (title, review, rating) (僅供 POST 用)
    處理邏輯: 
       - GET: 直接回傳表單畫面
       - POST: 驗證欄位是否補齊、呼叫 Book.create()、重導向回 '/'
    輸出: 渲染 templates/create.html (GET) 或重導向 (POST)
    """
    pass

@book_bp.route('/books/<int:id>')
def detail(id):
    """
    HTTP GET: 書籍詳情頁與留言清單
    輸入: URL variables `id`
    處理邏輯: 
       - 呼叫 Book.get_by_id(id) 取得對應書籍。
       - 呼叫 Comment.get_by_book_id(id) 取得底下關聯留言。
       - 若查無該書籍則觸發 404
    輸出: 渲染 templates/detail.html 並顯示相關資料
    """
    pass

@book_bp.route('/books/<int:id>/comments', methods=['POST'])
def add_comment(id):
    """
    HTTP POST: 發表留言
    輸入: URL variables `id` (作為 book_id), Form data `content`
    處理邏輯: 驗證留言內容非空、呼叫 Comment.create() 儲存資料
    輸出: 處理完畢後，重導向回指定書籍的詳情頁 ('/books/<id>')
    """
    pass
