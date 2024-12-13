import pytest
import numpy as np
from solveit.logic.sudoku import Sudoku, solve

@pytest.fixture
def valid_puzzle():
    return [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]

def test_solve_valid_puzzle(valid_puzzle):
    solution = solve(valid_puzzle)
    assert solution is not None
    assert len(solution) == 9
    assert len(solution[0]) == 9
    
    # Test rows
    for row in solution:
        assert sorted(row) == list(range(1, 10))
    
    # Test columns
    for col in range(9):
        column = [solution[row][col] for row in range(9)]
        assert sorted(column) == list(range(1, 10))

def test_invalid_puzzle_size():
    invalid_puzzle = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    with pytest.raises(ValueError):
        solver = Sudoku(invalid_puzzle)

def test_is_valid():
    solver = Sudoku([
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ])
    
    # Test valid placement
    assert solver.is_valid(4, (0, 2)) == True
    
    # Test invalid row
    assert solver.is_valid(5, (0, 2)) == False
    
    # Test invalid column
    assert solver.is_valid(3, (1, 0)) == False
    
    # Test invalid box
    assert solver.is_valid(9, (0, 1)) == False 