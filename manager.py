from pathlib import Path
import json

from objects import Task

class TaskManager:
    def __init__(self):
        self.json_path = self.json_init_and_get_path()
        self.task_obj_list = self.load_json(self.json_path)

    def json_init_and_get_path(self):
        app_dir = Path.home() / "AppData" / "Roaming" / "TaskManager"
        app_dir.mkdir(parents=True, exist_ok=True)
        json_path = app_dir / "tasks.json"

        if not json_path.exists():
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump([], f)
        
        return json_path
    
    def load_json(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            task_list = json.load(f)
        
        task_objects = []
        for task_dict in task_list:
            obj = Task.from_dict(task_dict)
            task_objects.append(obj)

        return task_objects

    def save_data(self):
        task_list = []
        for obj in self.task_obj_list:
            task = obj.to_dict()
            task_list.append(task)
            
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(task_list, f, indent=2, ensure_ascii=False)

    def list_tasks(self):
        for i in self.task_obj_list:
            print(i)

    def add_task(self, title):
        task = Task(title)
        self.task_obj_list.append(task)
        self.save_data()
