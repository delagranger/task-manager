from objects import Task
from objects import Group

from pathlib import Path
import json

class FileManager:
    def __init__(self):
        self.json_path = self.json_init_and_get_path()
        self.tasks, self.groups, self.next_task_id, self.next_group_id = self.load_data(self.json_path)

    def json_init_and_get_path(self):
        json_path = Path(
            "C:/Auguste/Projects/Python/task-manager/data/data.json"
            ) # сменить на рабочую директорию при необходимости
        json_format = {
            "next_task_id": 0, 
            "next_group_id": 0,
            "tasks": {},
            "groups": {}
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
            task = Task.from_dict(t)
            tasks.append(task)
        
        groups = []
        for g in data["groups"]:
            group = Group.from_dict(g)
            groups.append(group)

        return tasks, groups, data["next_task_id"], data["next_group_id"]

    def save_data(self):   
        tasks = []
        for t in self.tasks:
            task = t.to_dict()
            tasks.append(task)
        
        groups = []
        for g in self.groups:
            group = g.to_dict()
            groups.append(group)
        
        data = {
            "next_task_id": self.next_task_id, 
            "next_group_id": self.next_group_id,
            "tasks": tasks,
            "groups": groups
            }
            
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)