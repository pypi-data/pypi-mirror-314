import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
import tempfile
from pathlib import Path
import openpyxl

from solveit.data.cleaner import DataCleaner
from solveit.units.converter import UnitConverter, UnitType, UnitDefinition
from solveit.logic.sudoku import Sudoku, solve
from solveit.algorithms.pathfinding import PathFinder, Algorithm
from solveit.time.scheduler import Scheduler, Task, Priority, ResourceConflictError
from solveit.finance.calculator import FinancialCalculator
from solveit.viz.plotter import Plotter

# ============= Data Cleaner Tests =============
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'A': [1, 2, 2, None, 4, 100],
        'B': ['x', 'y', 'y', None, 'z', 'w'],
        'C': [1.1, 2.2, 2.2, 3.3, None, 4.4]
    })

@pytest.fixture
def temp_csv_file(sample_df):
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        sample_df.to_csv(tmp.name, index=False)
        return tmp.name

@pytest.fixture
def temp_excel_file(sample_df):
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        sample_df.to_excel(tmp.name, index=False)
        return tmp.name

def test_load_csv(temp_csv_file):
    cleaner = DataCleaner()
    df = cleaner.load_file(temp_csv_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 6
    assert list(df.columns) == ['A', 'B', 'C']
    os.unlink(temp_csv_file)

def test_load_excel(temp_excel_file):
    cleaner = DataCleaner()
    df = cleaner.load_file(temp_excel_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 6
    assert list(df.columns) == ['A', 'B', 'C']
    os.unlink(temp_excel_file)

def test_save_csv(sample_df):
    cleaner = DataCleaner()
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        cleaner.save_file(sample_df, tmp.name)
        loaded_df = pd.read_csv(tmp.name)
        assert len(loaded_df) == len(sample_df)
        assert list(loaded_df.columns) == list(sample_df.columns)
    os.unlink(tmp.name)

def test_save_excel(sample_df):
    cleaner = DataCleaner()
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        cleaner.save_file(sample_df, tmp.name)
        loaded_df = pd.read_excel(tmp.name)
        assert len(loaded_df) == len(sample_df)
        assert list(loaded_df.columns) == list(sample_df.columns)
    os.unlink(tmp.name)

def test_invalid_file_format():
    cleaner = DataCleaner()
    with tempfile.NamedTemporaryFile(suffix='.txt') as tmp:
        with pytest.raises(ValueError):
            cleaner.load_file(tmp.name)

def test_process_file(temp_csv_file):
    cleaner = DataCleaner()
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as output:
        cleaner.process_file(
            input_path=temp_csv_file,
            output_path=output.name,
            operations=[
                ('remove_duplicates', {}),
                ('handle_missing_values', {'strategy': 'mean'}),
                ('remove_outliers', {'columns': ['A'], 'method': 'zscore', 'threshold': 2.0})
            ]
        )
        result_df = pd.read_csv(output.name)
        assert len(result_df) == 4  # After removing duplicates and outliers
        assert not result_df['A'].isna().any()  # No missing values
    os.unlink(temp_csv_file)
    os.unlink(output.name)

# ============= Unit Converter Tests =============
@pytest.fixture
def converter():
    return UnitConverter()

def test_length_conversion(converter):
    # Test kilometers to miles
    result = converter.convert(100, "km", "mile", UnitType.LENGTH)
    assert round(result, 2) == 62.14
    
    # Test meters to feet
    result = converter.convert(1, "m", "ft", UnitType.LENGTH)
    assert round(result, 2) == 3.28

def test_mass_conversion(converter):
    # Test kilograms to pounds
    result = converter.convert(10, "kg", "lb", UnitType.MASS)
    assert round(result, 2) == 22.05

def test_digital_conversion(converter):
    # Test MB to KB
    result = converter.convert(1, "MB", "KB", UnitType.DIGITAL)
    assert result == 1024

def test_temperature_conversion(converter):
    # Test Celsius to Fahrenheit
    result = converter.convert(0, "C", "F", UnitType.TEMPERATURE)
    assert result == 32
    
    # Test Fahrenheit to Kelvin
    result = converter.convert(32, "F", "K", UnitType.TEMPERATURE)
    assert round(result, 2) == 273.15

# ============= Sudoku Tests =============
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

# ============= Pathfinding Tests =============
@pytest.fixture
def simple_graph():
    finder = PathFinder(Algorithm.DIJKSTRA)
    finder.add_edge("A", "B", 4)
    finder.add_edge("B", "C", 3)
    finder.add_edge("A", "C", 10)
    return finder

def test_dijkstra(simple_graph):
    path, distance = simple_graph.find_path("A", "C")
    assert path == ["A", "B", "C"]
    assert distance == 7

def test_a_star():
    finder = PathFinder(Algorithm.A_STAR)
    finder.add_edge("A", "B", 4)
    finder.add_edge("B", "C", 3)
    path, distance = finder.find_path("A", "C")
    assert path == ["A", "B", "C"]
    assert distance == 7

# ============= Scheduler Tests =============
@pytest.fixture
def scheduler():
    return Scheduler()

def test_add_task(scheduler):
    scheduler.add_task(
        name="Task 1",
        duration=timedelta(hours=2),
        priority=Priority.HIGH
    )
    assert "Task 1" in scheduler.tasks
    assert scheduler.tasks["Task 1"].priority == Priority.HIGH

def test_schedule_with_dependencies(scheduler):
    scheduler.add_task(
        name="Task 1",
        duration=timedelta(hours=2)
    )
    scheduler.add_task(
        name="Task 2",
        duration=timedelta(hours=3),
        dependencies=["Task 1"]
    )
    
    start_date = datetime(2024, 1, 1, 9, 0)
    schedule = scheduler.schedule(start_date)
    
    assert schedule["Task 1"]["start"] == start_date
    assert schedule["Task 2"]["start"] == schedule["Task 1"]["end"]

# ============= Financial Calculator Tests =============
@pytest.fixture
def calculator():
    return FinancialCalculator()

def test_compound_interest(calculator):
    result = calculator.compound_interest(
        principal=1000,
        rate=0.05,
        time=2,
        compounds_per_year=12
    )
    assert round(result['final_amount'], 2) == 1104.94
    assert round(result['interest_earned'], 2) == 104.94

def test_loan_payment(calculator):
    result = calculator.loan_payment(
        principal=100000,
        rate=0.05,
        years=30
    )
    assert round(result['monthly_payment'], 2) == 536.82
    assert round(result['total_interest'], 2) == 93255.78

def test_invalid_inputs(calculator):
    with pytest.raises(ValueError):
        calculator.compound_interest(
            principal=1000,
            rate=-0.05,
            time=1
        )
    
    with pytest.raises(ValueError):
        calculator.loan_payment(
            principal=-1000,
            rate=0.05,
            years=30
        )

# ============= Visualization Tests =============
@pytest.fixture
def sample_plot_data():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    return x.tolist(), y.tolist()

def test_line_plot(sample_plot_data):
    x, y = sample_plot_data
    plotter = Plotter()
    # Test that no exception is raised
    plotter.line_plot(
        x=x,
        y=y,
        title="Test Line Plot",
        xlabel="X",
        ylabel="Y"
    )

def test_scatter_plot(sample_plot_data):
    x, y = sample_plot_data
    plotter = Plotter()
    # Test that no exception is raised
    plotter.scatter_plot(
        x=x,
        y=y,
        title="Test Scatter Plot",
        xlabel="X",
        ylabel="Y"
    )

def test_invalid_plot_data():
    plotter = Plotter()
    with pytest.raises(ValueError):
        plotter.line_plot(
            x=[1, 2, 3],
            y=[1, 2]  # Mismatched lengths
        ) 