import os
os.environ['DB_TYPE'] = 'mysql'
os.environ['DB_NAME'] = 'library'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '3306'
os.environ['DB_USER'] = 'root'
os.environ['DB_PASSWORD'] = 'ezil'
import app
conn = app.get_db_connection()
print('connection ok')
conn.close()
