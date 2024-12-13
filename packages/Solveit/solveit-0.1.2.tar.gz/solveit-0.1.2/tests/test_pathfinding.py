import pytest
from solveit.algorithms.pathfinding import PathFinder, Algorithm

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

def test_invalid_path(simple_graph):
    path, distance = simple_graph.find_path("A", "D")
    assert path == []
    assert distance == float('infinity') 