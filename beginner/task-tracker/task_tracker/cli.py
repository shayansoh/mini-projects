from datetime import datetime
from typing import List, Optional
from task_tracker.models import Task, Status
from task_tracker.storage import Storage

class TaskCLI:
    def __init__(self, storage: Optional[Storage] = None):
        self.storage = storage or Storage()

    def add(self, description: str) -> Task:
        tasks = self.storage.load()
        task = Task(id=self.storage.next_id(), description=description)
        tasks.append(task)
        self.storage.save(tasks)
        print(f"Task added successfully (ID: {task.id})")
        return task
    
    def update(self, task_id: int, description: str) -> None:
        tasks = self.storage.load()
        for task in tasks:
            if task.id == task_id:
                task.description = description
                task.updated_at = datetime.now()
                self.storage.save(tasks)
                return
        raise ValueError(f"Task with ID {task_id} not found")
    
    def delete(self, task_id: int) -> None:
        tasks = self.storage.load()
        updated = [task for task in tasks if task.id != task_id]
        if len(updated) == len(tasks):
            raise ValueError(f"Task with ID {task_id} not found")
        self.storage.save(updated)

    def _set_status(self, task_id: int, status: Status) -> None:
        tasks = self.storage.load()
        for task in tasks:
            if task.id == task_id:
                task.status = status
                task.updated_at = datetime.now()
                self.storage.save(tasks)
                return
        raise ValueError(f"Task with ID {task_id} not found")
    
    def mark_in_progress(self, task_id: int) -> None:
        self._set_status(task_id, Status.IN_PROGRESS)

    def mark_done(self, task_id: int) -> None:
        self._set_status(task_id, Status.DONE)

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        tasks = self.storage.load()
        if status:
            tasks =  [task for task in tasks if task.status.value == status]
        if not tasks:
            print("No tasks found.")
            return []
        for task in tasks:
            print(f"[{task.id}] {task.description} ({task.status.value})")
        return tasks