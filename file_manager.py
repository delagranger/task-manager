from pathlib import Path
import json
import logging
import sys

from task import Task
from group import Group

log = logging.getLogger(__name__)

class FileManager:
    def __init__(self):
        self._json_path = self._json_init_and_get_path()
        self._data = self._load_json_data()

    def _json_init_and_get_path(self):
        json_path = Path(__file__).parent / "data" / "data.json"
        json_format = {"next_task_id": 0, 
                       "next_group_id": 1, 
                       "tasks": {}, 
                       "groups": [{"title": "default group", 
                                   "id": 0
                        }],
        }

        if not json_path.exists():
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_format, f, indent=2, ensure_ascii=False)
            log.info("JSON CREATED")
        
        return json_path

    def _load_json_data(self):
        try:
            with open(self._json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            log.debug("Load JSON: SUCCESS")
            return data
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
            log.critical("Load JSON: FAILED")
            log.critical("ERROR: %s", e)
            sys.exit(1)

    def load_ids(self):
        try:
            next_task_id = int(self._data["next_task_id"])
            next_group_id = int(self._data["next_group_id"])
            log.debug("Load ID`s: SUCCESS")
            return next_task_id, next_group_id
        except KeyError as e:
            log.critical("Load ID`s: FAILED")
            log.critical("ERROR: key not found %s", e)
            sys.exit(1)
        except (TypeError, ValueError) as e:
            log.critical("Load ID`s: FAILED")
            log.critical("ERROR: %s", e)
            sys.exit(1)
    
    def load_tasks(self):
        try:
            tasks = []
            for t in self._data["tasks"]:
                task = Task(t["title"], int(t["id"]), 
                            t["status"], t["group"],
                )
                tasks.append(task)
            log.debug("Load tasks: SUCCESS")
            return tasks
        except KeyError as e:
            log.critical("Load tasks: FAILED")
            log.critical("ERROR: key not found %s", e)
            sys.exit(1)
        except (TypeError, ValueError) as e:
            log.critical("Load tasks: FAILED")
            log.critical("ERROR: %s", e)
            sys.exit(1)
    
    def load_groups(self):
        try:
            groups = []
            for g in self._data["groups"]:
                group = Group(g["title"], int(g["id"]))
                groups.append(group)
            log.debug("Load groups: SUCCESS")
            return groups
        except KeyError as e:
            log.critical("Load groups: FAILED")
            log.critical("ERROR: key not found %s", e)
            sys.exit(1)
        except (TypeError, ValueError) as e:
            log.critical("Load groups: FAILED")
            log.critical("ERROR: %s", e)
            sys.exit(1)

    def save_data(self, tasks, groups, next_task_id, next_group_id):   
        tasks_list = []
        for t in tasks:
            task = t.to_dict()
            tasks_list.append(task)
        
        groups_list = []
        for g in groups:
            group = g.to_dict()
            groups_list.append(group)
        
        data = {"next_task_id": next_task_id, 
                "next_group_id": next_group_id, 
                "tasks": tasks_list, 
                "groups": groups_list,
        }
        
        try:
            with open(self._json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            log.debug("Save data: SUCCESS")
        except OSError as e:
            log.critical("Save data: FAILED")
            log.critical("ERROR: %s", e)