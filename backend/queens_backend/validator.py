class SolutionValidator:
    def __init__(self):
        self.board_size = 8
        self.debug = True

    def is_valid_solution(self, board_state):
        """Validate an 8-queens solution"""
        try:
            print(f"Validating board state: {board_state}")  # Debug log
            board = self._parse_board_state(board_state)
            print(f"Parsed board: {board}")  # Debug log

            # Check board size
            if not self._validate_dimensions(board):
                print("Invalid dimensions")  # Debug log
                return False

            # Count queens
            queens = self._get_queen_positions(board)
            if len(queens) != 8:
                print(f"Invalid queen count: {len(queens)}")  # Debug log
                return False

            # Check for conflicts
            for i, pos1 in enumerate(queens):
                row1, col1 = pos1
                for j in range(i + 1, len(queens)):
                    row2, col2 = queens[j]

                    # Check row and column
                    if row1 == row2 or col1 == col2:
                        print(f"Conflict between queens at {pos1} and {pos2}")  # Debug log
                        return False

                    # Check diagonals
                    if abs(row1 - row2) == abs(col1 - col2):
                        print(f"Diagonal conflict between queens at {pos1} and {pos2}")  # Debug log
                        return False

            return True

        except Exception as e:
            print(f"Error validating solution: {e}")  # Debug log
            return False

    def _parse_board_state(self, board_state):
        """Parse the board state string into a 2D array"""
        try:
            rows = board_state.split(';')
            board = [list(map(int, row.split(','))) for row in rows]
            return board
        except Exception as e:
            print(f"Error parsing board state: {e}")
            raise ValueError("Invalid board state format")

    def _validate_dimensions(self, board):
        """Check if the board dimensions are valid"""
        return len(board) == self.board_size and all(len(row) == self.board_size for row in board)

    def _get_queen_positions(self, board):
        """Extract queen positions from the board"""
        queens = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 1:
                    queens.append((i, j))
        return queens