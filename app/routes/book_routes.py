from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.book import Book
from app.models.comment import Comment

book_bp = Blueprint('book_routes', __name__)

@book_bp.route('/')
def index():
    """
    HTTP GET: 首頁 (列出所有書籍心得)
    """
    books = Book.get_all()
    return render_template('index.html', books=books)

@book_bp.route('/search')
def search():
    """
    HTTP GET: 搜尋書籍
    """
    q = request.args.get('q', '').strip()
    if q:
        books = Book.search_by_title(q)
    else:
        books = Book.get_all()
    return render_template('index.html', books=books, search_query=q)

@book_bp.route('/books/new', methods=['GET', 'POST'])
def create():
    """
    HTTP GET: 顯示新增書籍表單
    HTTP POST: 處理新增書籍邏輯
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        review = request.form.get('review', '').strip()
        rating_str = request.form.get('rating', '').strip()

        # 基本驗證: 檢查必填欄位
        if not title or not review or not rating_str:
            flash('提示：書名、心得與評分皆為必填欄位！', 'danger')
            return render_template('create.html', title=title, review=review, rating=rating_str)

        # 數值進階驗證
        try:
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                flash('提示：評分必須介於 1 到 5 之間', 'danger')
                return render_template('create.html', title=title, review=review, rating=rating_str)
        except ValueError:
            flash('提示：評分必須為數字', 'danger')
            return render_template('create.html', title=title, review=review, rating=rating_str)

        # 資料儲存
        try:
            Book.create(title, review, rating)
            flash('成功新增讀書心得！', 'success')
            return redirect(url_for('book_routes.index'))
        except Exception as e:
            flash(f'發生系統錯誤，無法新增：{e}', 'danger')
            return render_template('create.html', title=title, review=review, rating=rating_str)

    # 若為 GET 請求，單純渲染空白表單
    return render_template('create.html')

@book_bp.route('/books/<int:id>')
def detail(id):
    """
    HTTP GET: 書籍詳情頁與留言清單
    """
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該本讀書心得記錄！', 'danger')
        return redirect(url_for('book_routes.index'))
        
    comments = Comment.get_by_book_id(id)
    return render_template('detail.html', book=book, comments=comments)

@book_bp.route('/books/<int:id>/comments', methods=['POST'])
def add_comment(id):
    """
    HTTP POST: 發表留言
    """
    content = request.form.get('content', '').strip()
    
    # 留言不可為空值
    if not content:
        flash('留言內容不得為空白！', 'warning')
        return redirect(url_for('book_routes.detail', id=id))

    # 確認留言所屬的書籍是否存在
    book = Book.get_by_id(id)
    if not book:
        flash('書籍已被刪除，無法留言', 'danger')
        return redirect(url_for('book_routes.index'))

    # 資料寫入
    try:
        Comment.create(id, content)
        flash('留言發佈成功！', 'success')
    except Exception as e:
        flash(f'發生錯誤，無法發佈留言：{e}', 'danger')
        
    return redirect(url_for('book_routes.detail', id=id))
