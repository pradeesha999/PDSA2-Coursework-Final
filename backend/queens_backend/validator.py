class SolutionValidator:
    def __init__(self):
        self.board_size = 8

    def is_valid_solution(self, board_state):
        try:
            # Convert string board state to 2D array
            board = [[int(x) for x in row.split(',')] 
                    for row in board_state.split(';')]
            
            # Check board dimensions
            if len(board) != self.board_size or \
               any(len(row) != self.board_size for row in board):
                return False
            
            # Count queens
            queen_count = sum(sum(row) for row in board)
            if queen_count != self.board_size:
                return False

            # Check rows and columns
            for i in range(self.board_size):
                if sum(board[i]) != 1:  # Check row
                    return False
                if sum(row[i] for row in board) != 1:  # Check column
                    return False

            # Check diagonals
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if board[row][col] == 1:
                        if not self._check_diagonals(board, row, col):
                            return False

            return True
        except (ValueError, IndexError):
            return False

    def _check_diagonals(self, board, row, col):
        # Check diagonals
        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        for dx, dy in directions:
            x, y = row + dx, col + dy
            while 0 <= x < self.board_size and 0 <= y < self.board_size:
                if board[x][y] == 1:
                    return False
                x, y = x + dx, y + dy
        return True