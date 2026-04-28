from pathlib import Path
from typing import List
import json

from task_tracker.models import Task

class Storage:
    def __init__(self, file_path: Path = Path('tasks.json')):
        self.file_path = Path(file_path)

    def load(self) -> List[Task]:
        if not self.file_path.exists():
            return []
        with self.file_path.open('r') as f:
            data = json.load(f)
            return [Task.from_dict(item) for item in data]
        
    def save(self, tasks: List[Task]) -> None:
        with self.file_path.open('w') as f:
            json.dump([task.to_dict() for task in tasks], f, indent=4)

    def next_id(self) -> int:
        tasks = self.load()
        return max((task.id for task in tasks), default=0) + 1
    