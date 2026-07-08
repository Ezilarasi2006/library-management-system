
# Library Management System

A simple web-based Library Management System built with Python and Flask. It helps manage library users, books, and borrowing/returning transactions in a structured way.

## Features
- User registration and login
- Add, update, and delete books
- Borrow and return book transactions
- Dashboard with basic library statistics
- MySQL support and SQLite fallback for local testing

## Technologies Used
- Python
- Flask
- HTML/CSS
- MySQL
- PyMySQL
- Werkzeug

## Project Structure
- app.py - Main Flask application
- templates/ - HTML pages for login, registration, dashboard, books, and transactions
- static/ - CSS files
- tests/ - Basic test cases
- requirements.txt - Python dependencies

## Prerequisites
Make sure you have the following installed:
- Python 3.10 or above
- MySQL Server
- Git

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Ezilarasi2006/library-management-system.git
cd library-management-system
```

### 2. Create a virtual environment
On Windows:
```bash
python -m venv .venv
```

### 3. Activate the virtual environment
On Windows PowerShell:
```powershell
Activate.ps1
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

## Database Setup

This project uses MySQL by default.

### MySQL Configuration
Create the database first:
```sql
CREATE DATABASE library;
```

Then set the environment variables before running the app:
```powershell
$env:DB_TYPE="mysql"
$env:DB_NAME="library"
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
```

The app will create the required tables automatically when it starts.

### SQLite (Optional)
If you want to use SQLite instead, the app can also work with the local database file named library.db.

## Run the Application
Start the Flask server:
```bash
python app.py   -->.venv\Scripts\python.exe app.py                                                  
```

Open your browser and visit:
```text
http://127.0.0.1:5000/
```

## How to Use
1. Register a new account.
2. Log in with your credentials.
3. Add books to the system.
4. Borrow or return books from the transactions page.

## Running Tests
```bash
python -m unittest discover -s tests
```

## Troubleshooting
- If you see ERR_CONNECTION_REFUSED, the Flask server is not running.
- If the app uses SQLite instead of MySQL, check the database environment variables.
- If you get a MySQL connection error, check your MySQL username, password, host, and database name.
```
