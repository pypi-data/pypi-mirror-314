import pytest
from datetime import datetime, timedelta
from solveit.time.scheduler import Scheduler, Task, Priority, ResourceConflictError

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

def test_schedule_with_resources(scheduler):
    scheduler.add_task(
        name="Task 1",
        duration=timedelta(hours=2),
        resources=["Resource A"]
    )
    scheduler.add_task(
        name="Task 2",
        duration=timedelta(hours=2),
        resources=["Resource A"]
    )
    
    start_date = datetime(2024, 1, 1, 9, 0)
    schedule = scheduler.schedule(start_date)
    
    assert schedule["Task 2"]["start"] == schedule["Task 1"]["end"] 