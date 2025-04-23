import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': 'puzzle'
        }

    def get_connection(self):
        try:
            conn = mysql.connector.connect(**self.config)
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def execute_query(self, query, params=None):
        conn = self.get_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
            return result
        finally:
            cursor.close()
            conn.close()