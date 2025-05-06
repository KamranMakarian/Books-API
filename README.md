# 📚 **Books API**

A simple backend API built with **FastAPI**, demonstrating full **CRUD** operations using **SQLAlchemy** with a **MySQL** database.

---

## 🚀 Features

- Create, read, update, and delete books
- Associate books with authors
- Search books by title
- Pydantic models for validation
- Clean RESTful architecture
- JWT-ready structure for future authentication

---

## 🧰 Technologies

- FastAPI
- SQLAlchemy
- MySQL (via PyMySQL)
- Uvicorn
- Pydantic

---

## ⚙️ Getting Started

### 🖥️ Clone the Repository

```bash
git clone https://github.com/yourusername/Books-API.git
cd Books-API
```

### 🐍 Set Up Virtual Environment (Windows)

```bash
python -m venv venv
venv\Scripts\activate
```

### 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn SQLAlchemy pymysql python-multipart
```

---

### ▶️ Run the API

```bash
uvicorn main:app --reload
```

Then visit:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🗃️ MySQL Setup (If you're running locally)

### ✅ Start MySQL Server

1. Press `Windows` key → search for **Services**
2. Find `MySQL80` or `MySQL93`
3. Right-click → **Start**

### 🧪 Create Database via CLI

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Then:

```sql
CREATE DATABASE books;
SHOW DATABASES;
```

---

## 🧱 Configure `database.py`

Make sure to replace your MySql password in this line:

```python
engine = create_engine(
    'mysql+pymysql://root:YourPassword@localhost:3306/books',
    echo=True
)
```

Then create tables:

```bash
python database.py
```

---

## 🔎 API Endpoints

| Method | Endpoint               | Description                   |
| ------ | ---------------------- | ----------------------------- |
| GET    | `/`                    | Welcome message               |
| GET    | `/books`               | List all books with authors   |
| GET    | `/book/{book_id}`      | Get a specific book           |
| GET    | `/books/search?title=` | Search books by title         |
| POST   | `/book/`               | Add a book + author           |
| PUT    | `/book/{book_id}`      | Update a book's details       |
| DELETE | `/book/{book_id}`      | Delete a book and its pairing |

---

## 🧪 API Testing with Postman

You can import the included Postman collection to explore and test the API:

### 📁 File:

```
BooksAPIs.postman_collection.json
```

### 📥 How to Use:

1. Open [Postman](https://www.postman.com/)
2. Click **"Import"**
3. Select or drag the file:
   `BooksAPIs.postman_collection.json`
4. The collection will appear with preconfigured requests:

   * Add book
   * Get by ID
   * Update book
   * Delete book
   * Search by title
   * etc.

> All endpoints use `http://127.0.0.1:8000`, so make sure the API is running with:

```bash
uvicorn main:app --reload
```

---

## ✅ Notes and Future Improvements

* Don’t work inside the `venv/` directory
* Use `.gitignore` to avoid committing virtualenv or `.env` files
* Consider adding JWT authentication if needed

---

## 📢 Contributing
Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new branch (`feature/awesome-improvement`).
3. Commit and push your changes.
4. Open a pull request on GitHub describing your changes.

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).
Feel free to **modify, enhance, and contribute**!  

---

## 🙌 Acknowledgments

Created by **Kamran Makarian** as a learning project to explore FastAPI + SQLAlchemy integration.
Feel free to **connect and contribute**!
- **GitHub**: [KamranMakarian](https://github.com/KamranMakarian)  

---


