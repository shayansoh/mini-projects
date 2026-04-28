from task_tracker.storage import Storage
from task_tracker.models import Task, Status
import pytest

@pytest.fixture
def storage(tmp_path):
    return Storage(file_path=tmp_path / 'tasks.json')

# load()

def test_load_returns_empty_list_if_no_file(storage):
    assert storage.load() == []

def test_load_returns_tasks_from_file(storage):
    task = Task(id=1, description='Buy groceries')
    storage.save([task])
    tasks = storage.load()
    assert len(tasks) == 1
    assert tasks[0].description == 'Buy groceries'

def test_load_preserves_status(storage):
    task = Task(id=1, description="Buy groceries", status=Status.DONE)   
    storage.save([task])
    assert storage.load()[0].status == Status.DONE

# save()

def test_save_persists_multiple_tasks(storage):
    tasks = [
        Task(id=1, description='Task 1'),
        Task(id=2, description='Task 2')
    ]   
    storage.save(tasks)
    loaded = storage.load()
    assert len(loaded) == 2
    assert loaded[1].description == 'Task 2'

def test_save_overwrites_file(storage):
    storage.save([Task(id=1, description='Old task')])
    storage.save([Task(id=1, description='New task')])
    tasks = storage.load()
    assert len(tasks) == 1
    assert tasks[0].description == 'New task'

# next_id()

def test_next_id_starts_at_1_when_empty(storage):
    assert storage.next_id() == 1

def test_next_id_increments(storage):
    storage.save([Task(id=1, description="Task 1")])
    assert storage.next_id() == 2

def test_next_id_handles_gaps(storage):
    storage.save([Task(id=3, description="Task 3")])
    assert storage.next_id() == 4