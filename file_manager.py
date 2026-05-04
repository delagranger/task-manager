from objects import Task

from pathlib import Path
import json

class FileManager:
    def __init__(self):
        self.json_path = self.json_init_and_get_path()
        self.tasks = self.load_tasks(self.json_path)

    def json_init_and_get_path(self):
        app_dir = Path.home() / "AppData" / "Roaming" / "TaskManager"
        app_dir.mkdir(parents=True, exist_ok=True)
        json_path = app_dir / "tasks.json"

        if not json_path.exists():
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump([], f)
        
        return json_path
    
    def load_tasks(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            task_list = json.load(f)

        task_objects = []
        for t in task_list:
            t = Task.from_dict(t)
            task_objects.append(t)

        return task_objects
    
    def save_data(self):    
        task_list = []
        for t in self.tasks:
            task = t.to_dict()
            task_list.append(task)
            
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(task_list, f, indent=2, ensure_ascii=False)