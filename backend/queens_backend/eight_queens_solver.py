import threading
import time
from concurrent.futures import ThreadPoolExecutor

class QueensSolver:
    def __init__(self):
        self.solutions = []
        self.lock = threading.Lock()

    def is_safe(self, board, row, col):
        # Check row on left side
        for i in range(col):
            if board[row][i] == 1:
                return False
        
        # Check upper diagonal
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        
        # Check lower diagonal
        for i, j in zip(range(row, 8, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        
        return True

    def solve_sequential(self, board, col=0):
        if col >= 8:
            self.solutions.append([row[:] for row in board])
            return True

        for i in range(8):
            if self.is_safe(board, i, col):
                board[i][col] = 1
                self.solve_sequential(board, col + 1)
                board[i][col] = 0

        return False

    def solve_threaded(self, max_workers=4):
        def solve_partial(start_row):
            board = [[0 for _ in range(8)] for _ in range(8)]
            board[start_row][0] = 1
            self.solve_sequential(board, 1)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(solve_partial, range(8))

    def get_solutions(self):
        return self.solutions