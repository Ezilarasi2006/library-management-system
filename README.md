# Library Management System

A simple Flask-based library management system with:
- Login and registration
- Book CRUD operations
- Borrow and return transactions
- MySQL support with SQLite fallback for local testing

## Setup

1. Create a virtual environment:
   python -m venv .venv
2. Activate it:
   .venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Run the app:
   python app.py

## Database

By default the app uses SQLite file named library.db.
To use MySQL, set these environment variables before running:
- DB_TYPE=mysql
- DB_NAME=library
- DB_HOST=localhost
- DB_PORT=3306
- DB_USER=root
- DB_PASSWORD=yourpassword
