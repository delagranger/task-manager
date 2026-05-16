from pathlib import Path
import json
import logging
import sys

from task import Task
from group import Group

logger = logging.getLogger(__name__)

class FileManager:
    def __init__(self):
        self._json_path = self._json_init_and_get_path()
        self.data = self._load_json_data()

    def _json_init_and_get_path(self):
        json_path = Path(__file__).parent / "data" / "data.json"
        json_format = {
            "next_task_id": 0, 
            "next_group_id": 1,
            "tasks": [],
            "groups": [{
                "title": "ежедневные",
                "id": 0
                }]
            }

        if not json_path.exists():
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_format, f, indent=2, ensure_ascii=False)
            logger.info("JSON CREATED")
        
        return json_path
    
    def _load_json_data(self):
        try:
            with open(self._json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
            logger.error("Load JSON: failed")
            print(f"ERROR: {e}")
            sys.exit(1)

    def load_ids(self):
        try:
            next_task_id = int(self.data["next_task_id"])
            next_group_id = int(self.data["next_group_id"])
            logger.debug("Load ID`s: success")
            return next_task_id, next_group_id
        except KeyError as e:
            logger.error("Load ID`s: failed")
            print(f"ERROR: key not found: {e}")
            sys.exit(1)
        except (TypeError, ValueError) as e:
            logger.error("Load ID`s: failed")
            print(f"ERROR: {e}")
            sys.exit(1)
    
    def load_tasks(self):
        try:
            tasks = []
            for t in self.data["tasks"]:
                task = Task(t["title"], t["id"], t["status"],
                            t["group"]
                            )
                tasks.append(task)
            logger.debug("Load tasks: success")
            return tasks
        except KeyError as e:
            logger.error("Load tasks: failed")
            print(f"ERROR: key not found: {e}")
            sys.exit(1)
        except (TypeError, ValueError) as e:
            logger.error("Load tasks: failed")
            print(f"ERROR: {e}")
            sys.exit(1)
    
    def load_groups(self):
        try:
            groups = []
            for g in self.data["groups"]:
                group = Group(g["title"], g["id"])
                groups.append(group)
            logger.debug("Load groups: success")
            return groups
        except KeyError as e:
            logger.error("Load groups: failed")
            print(f"ERROR: key not found: {e}")
            sys.exit(1)
        except (TypeError, ValueError) as e:
            logger.error("Load groups: failed")
            print(f"ERROR: {e}")
            sys.exit(1)

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
        
        try:
            with open(self._json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Save data: success")
        except OSError as e:
            logger.error("Save data: failed")
            print(f"ERROR: {e}")