import pytest
from task_tracker.cli import TaskCLI
from task_tracker.models import Task, Status
from task_tracker.storage import Storage

@pytest.fixture
def cli(tmp_path):
    storage = Storage(file_path=tmp_path / "tasks.json")
    return TaskCLI(storage=storage)

# add()

def test_add_create_task(cli):
    cli.add("Buy groceries")
    tasks = cli.storage.load()
    assert len(tasks) == 1
    assert tasks[0].description == "Buy groceries"
    assert tasks[0].status == Status.TODO

def test_add_increments_id(cli):
    cli.add("Task 1")
    cli.add("Task 2")
    tasks = cli.storage.load()
    assert tasks[0].id == 1
    assert tasks[1].id == 2

# update()

def test_update_changes_description(cli):
    cli.add("Buy groceries")
    cli.update(1, "Buy fruits")
    assert cli.storage.load()[0].description == "Buy fruits"

def test_update_nonexistent_task_raises(cli):
    with pytest.raises(ValueError, match="not found"):
        cli.update(99, "Ghost task")

def test_update_refreshes_updated_at(cli):
    cli.add("Buy groceries")
    original = cli.storage.load()[0].updated_at
    cli.update(1, "Updated")
    updated = cli.storage.load()[0].updated_at
    assert updated >= original


# delete()

def test_delete_removes_task(cli):
    cli.add("Buy groceries")
    cli.delete(1)
    assert cli.storage.load() == []

def test_delete_nonexistent_task_raises(cli):
    with pytest.raises(ValueError, match="not found"):
        cli.delete(99)

def test_delete_only_removes_target(cli):
    cli.add("Task 1")
    cli.add("Task 2")
    cli.delete(1)
    tasks = cli.storage.load()
    assert len(tasks) == 1
    assert tasks[0].id == 2

# mark_in_progress() and mark_done()

def test_mark_in_progress(cli):
    cli.add("Buy groceries")
    cli.mark_in_progress(1)
    assert cli.storage.load()[0].status == Status.IN_PROGRESS

def test_mark_done(cli):
    cli.add("Buy groceries")
    cli.mark_done(1)
    assert cli.storage.load()[0].status == Status.DONE

def test_mark_nonexistent_raises(cli):
    with pytest.raises(ValueError, match="not found"):
        cli.mark_done(99)

# list_tasks()

def test_list_all_tasks(cli):
    cli.add("Task 1")
    cli.add("Task 2")
    tasks = cli.list_tasks()
    assert len(tasks) == 2

def test_list_filters_by_status(cli):
    cli.add("Task 1")
    cli.add("Task 2")
    cli.mark_done(1)
    done = cli.list_tasks(status="done")
    assert len(done) == 1
    assert done[0].id == 1

def test_list_empty_returns_empty(cli):
    assert cli.list_tasks() == []

def test_list_invalid_status_returns_empty(cli):
    cli.add("Task 1")
    tasks = cli.list_tasks(status="invalid")
    assert tasks == []