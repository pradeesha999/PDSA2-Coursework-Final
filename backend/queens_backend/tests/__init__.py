"""
Eight Queens Puzzle - Test Package
This package contains test cases for the Eight Queens Puzzle game.
"""

import os
import sys

# Add the parent directory to Python path for test imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test configuration
TEST_CONFIG = {
    'BOARD_SIZE': 8,
    'EXPECTED_SOLUTIONS': 92,
    'TEST_DB_NAME': 'eight_queens_test',
    'TEST_USER': 'testuser'
}

__all__ = ['TEST_CONFIG']