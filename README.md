
# Library Management System

A simple Library Management System built with Flask, MySQL, and HTML/CSS.

## Features
- User registration and login
- Add, update, and delete books
- Borrow and return book transactions
- Dashboard with counts of books and users
- MySQL database integration

## Technologies Used
- Python
- Flask
- MySQL
- PyMySQL
- HTML/CSS
- Werkzeug

## Project Structure
- app.py - Main Flask application
- templates/ - HTML templates
- static/ - CSS files
- tests/ - Basic test cases

## Installation
1. Clone the repository
   ```bash
   git clone https://github.com/Ezilarasi2006/library-management-system.git
   ```

2. Navigate to the project folder
   ```bash
   cd library-management-system
   ```

3. Create a virtual environment
   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

5. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup
Make sure MySQL is installed and running.

Update the database connection settings in app.py if needed:
- DB_TYPE
- DB_HOST
- DB_NAME
- DB_USER
- DB_PASSWORD

## Run the Application
```bash
python app.py
```

Open your browser and go to:
```text
http://127.0.0.1:5000/
```

## Usage
- Register a new account
- Log in
- Add books
- Borrow or return books

## License
This project is for educational purposes.
```

