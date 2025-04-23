"""
Eight Queens Puzzle - Main Package
This package contains the core functionality for the Eight Queens Puzzle game.
"""

from .validator import SolutionValidator
from .eight_queens_solver import QueensSolver
from .database import Database

__version__ = '1.0.0'
__author__ = 'Your Name'

# Export main classes
__all__ = ['SolutionValidator', 'QueensSolver', 'Database']