from task_tracker.models import Task, Status

def test_task_default_status():
    task = Task(id=1, description='Buy groceries')
    assert task.status == Status.TODO

def test_task_has_timestamps():
    task = Task(id=1, description='Buy groceries')
    assert task.created_at is not None
    assert task.updated_at is not None

def test_to_dict_shape():
    task = Task(id=1, description='Buy groceries')
    d = task.to_dict()
    assert d['id'] == 1
    assert d['description'] == 'Buy groceries'
    assert d['status'] == 'todo'
    assert 'created_at' in d
    assert 'updated_at' in d

def test_to_dict_status_is_string():
    task = Task(id=1, description="Buy groceries", status=Status.IN_PROGRESS)
    assert task.to_dict()["status"] == "in-progress"

def test_from_dict_round_trip():
    task = Task(id=1, description="Buy groceries")
    restored = Task.from_dict(task.to_dict())
    assert restored.id == task.id
    assert restored.description == task.description
    assert restored.status == task.status
    assert restored.created_at == task.created_at

def test_from_dict_parses_status():
    data = {
        "id": 2,
        "description": "Cook dinner",
        "status": "done",
        "created_at": "2024-01-01T10:00:00",
        "updated_at": "2024-01-01T10:00:00"
    }
    task = Task.from_dict(data)
    assert task.status == Status.DONE