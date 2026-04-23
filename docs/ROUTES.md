# 路由與頁面設計 (Routes Design)

## 1. 路由總覽表格

本系統的路由採用 RESTful 風格設計，並配合 HTML 表單 (GET 讀取畫面，POST 提交資料) 的特性切分功能：

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (書籍清單) | GET | `/` | `index.html` | 列出所有書籍與心得（預設按最新排序） |
| 搜尋書籍 | GET | `/search` | `index.html` | 接收 `q` 參數搜尋書籍，並可重複利用首頁模板呈現列出結果 |
| 新增書籍表單 | GET | `/books/new` | `create.html` | 呈現包含書籍名稱、心得、評分的輸入表單介面 |
| 送出新增書籍 | POST | `/books/new` | — | 接收並儲存書籍資料，成功後重新導向至首頁 |
| 書籍詳情頁 | GET | `/books/<int:id>` | `detail.html` | 顯示單一書籍的完整心得內容，以及所有人在底下的留言紀錄 |
| 送出新增留言 | POST | `/books/<int:id>/comments` | — | 接收特定書籍的留言表單資料並儲存，成功後重新導向至該書籍詳情頁 |

---

## 2. 每個路由的詳細說明

### 首頁 (書籍清單) - `GET /`
- **輸入**：無
- **處理邏輯**：呼叫 `app.models.book.Book.get_all()` 取得所有書籍的字典清單。
- **輸出**：渲染 `index.html`，將書籍清單資料帶入 Jinja2 變數渲染畫面。
- **錯誤處理**：如果資料庫存取失敗顯示 500 系統錯誤。

### 搜尋書籍 - `GET /search`
- **輸入**：URL 參數字串 (Query String) `q`，例如 `?q=書籍名稱`。
- **處理邏輯**：從 Request 中取得 `q`，若有值則呼叫 `Book.search_by_title(q)`；若無值則導向一般的首頁全資料清單。
- **輸出**：將搜尋完的結果拋回給 `index.html` 中渲染顯示。
- **錯誤處理**：無相符結果時顯示空清單提示訊息。

### 新增書籍表單 / 送出新增書籍 - `GET & POST /books/new`
- **輸入**：GET 時無參數；POST 時傳遞 Form 表單欄位：`title`, `review`, `rating`。
- **處理邏輯**：
  - GET 時僅呈現畫面。
  - POST 時於後端驗證三個必填參數是否存在。若驗證成功，則呼叫 `Book.create(title, review, rating)`，並將使用者重導向回首頁 (`/`)。
- **輸出**：GET 渲染 `create.html`。POST重導向 `index` 路由。
- **錯誤處理**：若有漏傳欄位，則建立錯誤訊息字串 (Flash) 帶回 `create.html`，讓使用者重新填寫。

### 書籍詳情頁 - `GET /books/<int:id>`
- **輸入**：URL路徑包含特定書籍的整數 ID。
- **處理邏輯**：透過 `Book.get_by_id(id)` 查詢書籍詳細資訊；並呼叫 `Comment.get_by_book_id(id)` 抓取該書底下關聯的留言列表。
- **輸出**：將書籍與所有留言打包後傳入 `detail.html` 進行渲染顯示。
- **錯誤處理**：如果該 ID 在資料庫查無紀錄，則回傳 `404 Not Found`。

### 送出新增留言 - `POST /books/<int:id>/comments`
- **輸入**：URL 上的書籍 `id` 以及表單中的 `content` 欄位。
- **處理邏輯**：簡易防空值驗證後，呼叫 `Comment.create(book_id, content)` 將留言儲存進資料庫。
- **輸出**：儲存成功後進行轉址重導向，至 `detail` 路由 (路徑 `/books/<id>`)，讓畫面呈現最新寫入的留言。
- **錯誤處理**：若留言內容為空，利用 Flash 產生提示，並放棄寫入，同樣重導回書籍詳情頁。

---

## 3. Jinja2 模板清單

所有 HTML 模板將放置於 `app/templates/` 中。架構上，所有具體頁面將會繼承 `base.html` 提供的佈局與樣式。

1. **`base.html`**：核心母版。包含 `<head>`、全局共用之導覽列 (標題、"新增"連結與搜尋輸入框)、共用頁尾及共用 CSS 引入。並留有 `{% block content %}` 區塊供子頁面安插內容。
2. **`index.html`**（首頁/列表）：繼承 `base.html`。負責歷遍並生成「書籍卡片清單」，如果接收到的資料為空則顯示一段親切友善的提醒訊息。
3. **`create.html`**（新增頁面）：繼承 `base.html`。提供包含 書名 (text)、心得 (textarea)、評分 (number 或 select) 及送出按鈕的 HTML Form 表單。
4. **`detail.html`**（詳情頁面）：繼承 `base.html`。畫面區分為上下層：上層呈現這本書的完整名稱、心得及星星數；下層則列出每則留言與時間，且頁尾有一個新的 Form 表單供撰寫新留言。

---

## 4. 路由骨架程式碼

路由實作會切分於 `app/routes/` 內。為保持擴充性與整潔，我們會採用 Flask 的 Blueprints 結構。以下骨架已經為您存入 `app/routes/book_routes.py`。
