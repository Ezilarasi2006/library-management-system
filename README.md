
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
## output:
<img width="470" height="172" alt="image" src="https://github.com/user-attachments/assets/8c49847e-f263-485b-b103-bbebe7785b73" />
<img width="464" height="181" alt="image" src="https://github.com/user-attachments/assets/97fa9afe-b676-4797-8b12-a37aa7365251" />
<img width="460" height="201" alt="image" src="https://github.com/user-attachments/assets/befe1cd0-203d-4a88-8b27-687ec09bb634" />
<img width="468" height="217" alt="image" src="https://github.com/user-attachments/assets/68444f82-e23c-4f92-920a-2cdecbe02177" />
<img width="466" height="217" alt="image" src="https://github.com/user-attachments/assets/ad617a88-ea61-4bdf-9206-facfb535c6c4" />
<img width="469" height="155" alt="image" src="https://github.com/user-attachments/assets/e2bf752b-fc2f-42d3-85b3-98e8c85d2dc0" />
<img width="467" height="332" alt="image" src="https://github.com/user-attachments/assets/c31805b3-ab52-4e8e-9292-d29c4d077bb3" />







