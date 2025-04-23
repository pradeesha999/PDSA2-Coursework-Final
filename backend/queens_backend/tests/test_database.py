import mysql.connector
import pytest

class TestDatabase:
    @pytest.fixture(autouse=True)
    def setup_database(self):
        # Connect to the database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="puzzle"
        )
        self.cursor = self.connection.cursor()

        # Create the test_solutions table if it doesn't exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_solutions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            solution VARCHAR(255) NOT NULL
        )
        """)

        yield

        # Cleanup: Drop the test_solutions table after the test
        self.cursor.execute("DROP TABLE IF EXISTS test_solutions")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def test_execute_query(self):
        # Test INSERT
        self.cursor.execute(
            "INSERT INTO test_solutions (solution) VALUES (%s)",
            ("test_solution",)
        )
        self.connection.commit()

        # Test SELECT
        self.cursor.execute(
            "SELECT * FROM test_solutions WHERE solution = %s",
            ("test_solution",)
        )
        result = self.cursor.fetchall()
        assert len(result) == 1
        assert result[0][1] == "test_solution"