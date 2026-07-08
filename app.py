import os
import sqlite3
from datetime import datetime

import pymysql.cursors
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "library-secret-key")

DB_TYPE = os.environ.get("DB_TYPE", "mysql").lower()
DB_NAME = os.environ.get("DB_NAME", "library" if DB_TYPE == "mysql" else "library.db")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "ezil")
print(f"Using database backend: {DB_TYPE} | database: {DB_NAME}")


def get_db_connection(include_database=True):
    if DB_TYPE == "mysql":
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME if include_database else None,
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor,
            )
            return conn
        except Exception as exc:
            print(f"MySQL connection failed: {exc}")
            raise

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def db_execute(conn, query, params=()):
    if DB_TYPE == "mysql":
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor

    normalized_query = query.replace("%s", "?")
    return conn.execute(normalized_query, params)


def db_fetch_all(conn, query, params=()):
    cursor = db_execute(conn, query, params)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def db_fetch_one(conn, query, params=()):
    cursor = db_execute(conn, query, params)
    row = cursor.fetchone()
    cursor.close()
    return row


def init_db():
    if DB_TYPE == "mysql":
        conn = get_db_connection(include_database=False)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        conn.commit()
        conn.close()

    conn = get_db_connection()
    cur = conn.cursor()

    if DB_TYPE == "mysql":
        users_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL
        )
        """
        books_sql = """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            isbn VARCHAR(255) NOT NULL UNIQUE,
            category VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            available_quantity INT NOT NULL
        )
        """
        transactions_sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT NOT NULL,
            user_id INT NOT NULL,
            transaction_type VARCHAR(50) NOT NULL,
            transaction_date VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    else:
        users_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
        """
        books_sql = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            available_quantity INTEGER NOT NULL
        )
        """
        transactions_sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            transaction_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """

    cur.execute(users_sql)
    cur.execute(books_sql)
    cur.execute(transactions_sql)
    conn.commit()
    conn.close()


init_db()


def login_required(view):
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


@app.route("/")
@login_required
def index():
    conn = get_db_connection()
    books = db_fetch_all(conn, "SELECT * FROM books ORDER BY id DESC")
    transactions = db_fetch_all(
        conn,
        """
        SELECT t.*, b.title, u.username
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        JOIN users u ON t.user_id = u.id
        ORDER BY t.id DESC
        LIMIT 20
        """,
    )
    total_books = db_fetch_one(conn, "SELECT COUNT(*) as count FROM books")["count"]
    total_users = db_fetch_one(conn, "SELECT COUNT(*) as count FROM users")["count"]
    conn.close()
    return render_template("index.html", books=books, transactions=transactions, total_books=total_books, total_users=total_users)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))

        conn = get_db_connection()
        existing = db_fetch_one(conn, "SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        if existing:
            conn.close()
            flash("Username or email already exists.", "danger")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)
        try:
            db_execute(
                conn,
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash),
            )
            conn.commit()
        except Exception as exc:
            conn.rollback()
            print(f"User insert failed: {exc}")
            flash("Could not save user to MySQL. Check the terminal for details.", "danger")
            return redirect(url_for("register"))
        conn.close()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db_connection()
        user = db_fetch_one(conn, "SELECT * FROM users WHERE username = %s", (username,))
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful.", "success")
            return redirect(url_for("index"))

        flash("Invalid username or password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out.", "info")
    return redirect(url_for("login"))


@app.route("/books", methods=["GET", "POST"])
@login_required
def books():
    conn = get_db_connection()
    if request.method == "POST":
        book_id = request.form.get("book_id")
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()
        category = request.form.get("category", "").strip()
        quantity = int(request.form.get("quantity", 0) or 0)

        if request.form.get("delete_id"):
            db_execute(conn, "DELETE FROM books WHERE id = %s", (request.form.get("delete_id"),))
            conn.commit()
            conn.close()
            flash("Book deleted.", "success")
            return redirect(url_for("books"))

        if not all([title, author, isbn, category]) or quantity < 1:
            conn.close()
            flash("Please enter valid book details.", "danger")
            return redirect(url_for("books"))

        existing_book = db_fetch_one(conn, "SELECT id FROM books WHERE isbn = %s", (isbn,))
        if existing_book and not book_id:
            conn.close()
            flash("A book with this ISBN already exists. Please use a different ISBN.", "danger")
            return redirect(url_for("books"))

        try:
            if book_id:
                db_execute(
                    conn,
                    "UPDATE books SET title = %s, author = %s, isbn = %s, category = %s, quantity = %s, available_quantity = %s WHERE id = %s",
                    (title, author, isbn, category, quantity, quantity, book_id),
                )
                flash("Book updated.", "success")
            else:
                db_execute(
                    conn,
                    "INSERT INTO books (title, author, isbn, category, quantity, available_quantity) VALUES (%s, %s, %s, %s, %s, %s)",
                    (title, author, isbn, category, quantity, quantity),
                )
                flash("Book added.", "success")

            conn.commit()
        except Exception as exc:
            conn.rollback()
            print(f"Book insert failed: {exc}")
            flash("Could not save book to MySQL. Check the terminal for details.", "danger")
            return redirect(url_for("books"))
        conn.close()
        return redirect(url_for("books"))

    edit_id = request.args.get("edit")
    edit_book = None
    if edit_id:
        edit_book = db_fetch_one(conn, "SELECT * FROM books WHERE id = %s", (edit_id,))
    books_list = db_fetch_all(conn, "SELECT * FROM books ORDER BY id DESC")
    conn.close()
    return render_template("books.html", books=books_list, edit_book=edit_book)


@app.route("/transactions", methods=["GET", "POST"])
@login_required
def transactions():
    conn = get_db_connection()
    if request.method == "POST":
        book_id = request.form.get("book_id")
        transaction_type = request.form.get("transaction_type")
        user_id = session["user_id"]

        book = db_fetch_one(conn, "SELECT * FROM books WHERE id = %s", (book_id,))
        if not book:
            conn.close()
            flash("Book not found.", "danger")
            return redirect(url_for("transactions"))

        if transaction_type == "borrow":
            if book["available_quantity"] <= 0:
                conn.close()
                flash("This book is currently unavailable.", "danger")
                return redirect(url_for("transactions"))
            new_available = book["available_quantity"] - 1
            status = "Borrowed"
        else:
            new_available = book["available_quantity"] + 1
            status = "Returned"

        db_execute(
            conn,
            "UPDATE books SET available_quantity = %s WHERE id = %s",
            (new_available, book_id),
        )
        db_execute(
            conn,
            """
            INSERT INTO transactions (book_id, user_id, transaction_type, transaction_date, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (book_id, user_id, transaction_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status),
        )
        conn.commit()
        conn.close()
        flash("Transaction recorded.", "success")
        return redirect(url_for("transactions"))

    books_list = db_fetch_all(conn, "SELECT * FROM books ORDER BY id DESC")
    transactions_list = db_fetch_all(
        conn,
        """
        SELECT t.*, b.title, u.username
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        JOIN users u ON t.user_id = u.id
        ORDER BY t.id DESC
        """,
    )
    conn.close()
    return render_template("transactions.html", books=books_list, transactions=transactions_list)


if __name__ == "__main__":
    app.run(debug=True)
