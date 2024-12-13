import pytest
import numpy as np
from solveit.viz.plotter import Plotter

@pytest.fixture
def sample_data():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    return x.tolist(), y.tolist()

def test_line_plot(sample_data):
    x, y = sample_data
    plotter = Plotter()
    # Test that no exception is raised
    plotter.line_plot(
        x=x,
        y=y,
        title="Test Line Plot",
        xlabel="X",
        ylabel="Y"
    )

def test_scatter_plot(sample_data):
    x, y = sample_data
    plotter = Plotter()
    # Test that no exception is raised
    plotter.scatter_plot(
        x=x,
        y=y,
        title="Test Scatter Plot",
        xlabel="X",
        ylabel="Y"
    )

def test_invalid_data():
    plotter = Plotter()
    with pytest.raises(ValueError):
        plotter.line_plot(
            x=[1, 2, 3],
            y=[1, 2]  # Mismatched lengths
        ) 