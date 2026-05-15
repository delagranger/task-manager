from pathlib import Path
import json
import logging

from task import Task
from group import Group

logger = logging.getLogger(__name__)

class FileManager:
    def __init__(self):
        self._json_path = self._json_init_and_get_path()

    def _json_init_and_get_path(self):
        json_path = Path(__file__).parent / "data" / "data.json"
        json_format = {
            "next_task_id": 0, 
            "next_group_id": 0,
            "tasks": {},
            "groups": {}
            }

        if not json_path.exists():
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_format, f, indent=2, ensure_ascii=False)
            logger.info("JSON CREATED")
        
        return json_path
    
    def load_ids(self):
        with open(self._json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.debug("Load ID`s: success")
        return data["next_task_id"], data["next_group_id"]
    
    def load_tasks(self):
        with open(self._json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        tasks = []
        for t in data["tasks"]:
            task = Task(t["title"], t["id"], t["status"],
                        t["group"]
                        )
            tasks.append(task)
        
        logger.debug("Load tasks: success")
        return tasks
    
    def load_groups(self):   
        with open(self._json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        groups = []
        for g in data["groups"]:
            group = Group(g["title"], g["id"])
            groups.append(group)
        
        logger.debug("Load groups: success")
        return groups

    def save_data(self, tasks, groups,
                  next_task_id,
                  next_group_id
                  ):   
        tasks_list = []
        for t in tasks:
            task = t.to_dict()
            tasks_list.append(task)
        
        groups_list = []
        for g in groups:
            group = g.to_dict()
            groups_list.append(group)
        
        data = {
            "next_task_id": next_task_id, 
            "next_group_id": next_group_id,
            "tasks": tasks_list,
            "groups": groups_list
            }
            
        with open(self._json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info("DATA SAVED")