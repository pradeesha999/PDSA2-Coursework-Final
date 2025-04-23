import unittest
import time
from backend.queens_backend.eight_queens_solver import QueensSolver

class TestQueensSolver(unittest.TestCase):
    def setUp(self):
        self.solver = QueensSolver()

    def test_performance_comparison(self):
        # Run multiple times to get average performance
        runs = 5
        sequential_times = []
        threaded_times = []

        for _ in range(runs):
            # Test sequential
            start_time = time.time()
            board = [[0 for _ in range(8)] for _ in range(8)]
            self.solver.solve_sequential(board)
            sequential_times.append(time.time() - start_time)

            # Reset solver
            self.solver = QueensSolver()

            # Test threaded
            start_time = time.time()
            self.solver.solve_threaded()
            threaded_times.append(time.time() - start_time)

        avg_sequential = sum(sequential_times) / runs
        avg_threaded = sum(threaded_times) / runs

        # Compare average times with some tolerance
        self.assertLessEqual(avg_threaded, avg_sequential * 1.5)