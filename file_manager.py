from objects import Task

from pathlib import Path
import json

class FileManager:
    def __init__(self):
        self.json_path = self.json_init_and_get_path()
        self.tasks, self.next_task_id = self.load_data(self.json_path)

    def json_init_and_get_path(self):
        app_dir = Path.home() / "AppData" / "Roaming" / "TaskManager"
        app_dir.mkdir(parents=True, exist_ok=True)
        json_path = app_dir / "data.json"
        json_format = {
            "next_task_id": 0, 
            "tasks": {}
            }

        if not json_path.exists():
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_format, f, indent=2, ensure_ascii=False)
        
        return json_path
    
    def load_data(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        tasks = []
        for t in data["tasks"]:
            t = Task.from_dict(t)
            tasks.append(t)

        return tasks, data["next_task_id"]

    def save_data(self):   
        tasks = []

        for t in self.tasks:
            task = t.to_dict()
            tasks.append(task)
        
        data = {
            "next_task_id": self.next_task_id, 
            "tasks": tasks
            }
            
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)