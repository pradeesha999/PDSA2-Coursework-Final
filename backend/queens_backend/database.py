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
        self.connection = self.get_connection()

    def get_connection(self):
        try:
            conn = mysql.connector.connect(**self.config)
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            print(f"Executing query: {query}")  # Debug log
            print(f"With parameters: {params}")  # Debug log
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")  # Debug log
            return None