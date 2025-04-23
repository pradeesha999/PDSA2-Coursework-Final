class SolutionValidator:
    @staticmethod
    def is_valid_solution(board_state):
        try:
            # Convert string board state to 2D array
            board = [[int(x) for x in row.split(',')] 
                    for row in board_state.split(';')]
            
            # Validate board dimensions
            if len(board) != 8 or any(len(row) != 8 for row in board):
                return False
            
            # Count queens
            queen_count = sum(sum(row) for row in board)
            if queen_count != 8:
                return False

            # Check rows and columns
            for i in range(8):
                if sum(board[i]) != 1:  # Check row
                    return False
                if sum(row[i] for row in board) != 1:  # Check column
                    return False

            # Check diagonals
            for row in range(8):
                for col in range(8):
                    if board[row][col] == 1:
                        # Check diagonals
                        if not SolutionValidator._check_diagonals(board, row, col):
                            return False

            return True
        except (ValueError, IndexError):
            return False

    @staticmethod
    def _check_diagonals(board, row, col):
        # Check all diagonals from position (row, col)
        for i, j in [(i, j) for i in range(8) for j in range(8)]:
            if i != row and j != col and board[i][j] == 1:
                if abs(row - i) == abs(col - j):
                    return False
        return True

import unittest
from backend.queens_backend.validator import SolutionValidator

class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = SolutionValidator()
        self.valid_solution = "0,0,0,0,1,0,0,0;0,0,0,0,0,0,1,0;0,0,0,1,0,0,0,0;0,0,0,0,0,0,0,1;0,1,0,0,0,0,0,0;0,0,0,0,0,1,0,0;1,0,0,0,0,0,0,0;0,0,1,0,0,0,0,0"

    def test_valid_solution(self):
        """Test a known valid solution"""
        self.assertTrue(self.validator.is_valid_solution(self.valid_solution))

    def test_invalid_dimensions(self):
        """Test board with wrong dimensions"""
        invalid_board = "0,0,0;0,0,0;0,0,0"
        self.assertFalse(self.validator.is_valid_solution(invalid_board))

    def test_invalid_queen_count(self):
        """Test board with wrong number of queens"""
        too_many_queens = "1,1,0,0,0,0,0,0;0,0,0,0,0,0,1,0;0,0,0,1,0,0,0,0;0,0,0,0,0,0,0,1;0,1,0,0,0,0,0,0;0,0,0,0,0,1,0,0;1,0,0,0,0,0,0,0;0,0,1,0,0,0,0,0"
        self.assertFalse(self.validator.is_valid_solution(too_many_queens))

    def test_invalid_diagonal(self):
        """Test queens attacking on diagonal"""
        diagonal_attack = "1,0,0,0,0,0,0,0;0,1,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0"
        self.assertFalse(self.validator.is_valid_solution(diagonal_attack))

if __name__ == '__main__':
    unittest.main()