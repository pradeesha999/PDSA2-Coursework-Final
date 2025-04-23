import pytest
from backend.database import Database

@pytest.fixture(scope="module")
def db():
    # ...existing code...
    db = Database()
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS test_solutions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            solution TEXT NOT NULL,
            is_valid BOOLEAN NOT NULL DEFAULT TRUE
        );
    """)
    return db

def test_execute_query(db):
    # ...existing code...
    result = db.execute_query("SELECT * FROM test_solutions;")
    assert result is not None
