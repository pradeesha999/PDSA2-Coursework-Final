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

    def _is_safe(self, board, row, col):
        """Check if a queen at position (row, col) is safe"""
        # Check all diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Top-left, top-right, bottom-left, bottom-right
        for dx, dy in directions:
            x, y = row, col
            while 0 <= x < self.board_size and 0 <= y < self.board_size:
                x += dx
                y += dy
                if 0 <= x < self.board_size and 0 <= y < self.board_size and board[x][y] == 1:
                    return False
        return True

import unittest
from backend.queens_backend.validator import SolutionValidator

class TestValidator(unittest.TestCase):
    def setUp(self):
        """Initialize validator and test data"""
        self.validator = SolutionValidator()
        
        # Known valid solutions
        self.valid_solutions = [
            "0,0,0,0,1,0,0,0;0,0,0,0,0,0,1,0;0,0,0,1,0,0,0,0;0,0,0,0,0,0,0,1;0,1,0,0,0,0,0,0;0,0,0,0,0,1,0,0;1,0,0,0,0,0,0,0;0,0,1,0,0,0,0,0",
            "1,0,0,0,0,0,0,0;0,0,0,0,1,0,0,0;0,0,0,0,0,0,0,1;0,0,0,0,0,1,0,0;0,0,1,0,0,0,0,0;0,0,0,0,0,0,1,0;0,1,0,0,0,0,0,0;0,0,0,1,0,0,0,0"
        ]
        
        # Known invalid solutions
        self.invalid_solutions = {
            "row_conflict": "1,1,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0",
            "column_conflict": "1,0,0,0,0,0,0,0;1,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0",
            "diagonal_conflict": "1,0,0,0,0,0,0,0;0,1,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0",
            "wrong_size": "1,0,0;0,1,0;0,0,1",
            "too_many_queens": "1,1,1,1,1,1,1,1;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0",
            "too_few_queens": "1,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0"
        }

    def test_valid_solutions(self):
        """Test known valid solutions"""
        for solution in self.valid_solutions:
            with self.subTest(solution=solution):
                self.assertTrue(
                    self.validator.is_valid_solution(solution),
                    f"Valid solution was rejected: {solution}"
                )

    def test_invalid_dimensions(self):
        """Test board with wrong dimensions"""
        self.assertFalse(
            self.validator.is_valid_solution(self.invalid_solutions["wrong_size"]),
            "Board with wrong dimensions was accepted"
        )

    def test_row_conflict(self):
        """Test queens in same row"""
        self.assertFalse(
            self.validator.is_valid_solution(self.invalid_solutions["row_conflict"]),
            "Queens in same row were accepted"
        )

    def test_column_conflict(self):
        """Test queens in same column"""
        self.assertFalse(
            self.validator.is_valid_solution(self.invalid_solutions["column_conflict"]),
            "Queens in same column were accepted"
        )

    def test_diagonal_conflict(self):
        """Test queens on same diagonal"""
        self.assertFalse(
            self.validator.is_valid_solution(self.invalid_solutions["diagonal_conflict"]),
            "Queens on same diagonal were accepted"
        )

    def test_queen_count(self):
        """Test incorrect number of queens"""
        self.assertFalse(
            self.validator.is_valid_solution(self.invalid_solutions["too_many_queens"]),
            "Too many queens were accepted"
        )
        self.assertFalse(
            self.validator.is_valid_solution(self.invalid_solutions["too_few_queens"]),
            "Too few queens were accepted"
        )

    def test_malformed_input(self):
        """Test invalid input formats"""
        invalid_inputs = [
            "",  # Empty string
            "invalid",  # Invalid format
            "1,2,3;4,5,6",  # Invalid numbers
            "a,b,c;d,e,f",  # Non-numeric
            None,  # None input
        ]
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                self.assertFalse(
                    self.validator.is_valid_solution(invalid_input),
                    f"Invalid input was accepted: {invalid_input}"
                )

if __name__ == '__main__':
    unittest.main()