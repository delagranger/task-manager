from operator import attrgetter
import logging

from task import Task
from group import Group
from file_manager import FileManager
from validators import Validator, ValidationError

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self):
        self._file_manager = FileManager()
        self._validator = Validator(self)
        self._next_task_id, self._next_group_id = self._file_manager.load_ids()
        self._tasks = self._file_manager.load_tasks()
        self._groups = self._file_manager.load_groups()

    def add_task(self, title, status, group):
        try:
            self._validator.is_group_exists(group)
            
            task = Task(title, 
                        self._next_task_id,
                        status, group
                        )
            self._next_task_id += 1
            self._tasks.append(task)
            logger.info("add-task: SUCCESS")

            self._file_manager.save_data(self._tasks, self._groups,
                                        self._next_task_id,
                                        self._next_group_id
                                        )
        except ValidationError as e:
            logger.error("add-task: FAILED")
            print(f"ERROR: {e}")

    def add_group(self, title):
        try:
            self._validator.is_group_not_exists(title)

            group = Group(title,
                        self._next_group_id
                        )
            self._next_group_id += 1
            self._groups.append(group)
            logger.info("add-group: SUCCESS")

            self._file_manager.save_data(self._tasks, self._groups,
                                        self._next_task_id,
                                        self._next_group_id
                                        )
        except ValidationError as e:
            logger.error("add-group: FAILED")
            print(f"ERROR: {e}")

    def list_tasks(self, sort_type, status, group, filtered=False):
        filtered_tasks = self._tasks
        try:
            if filtered:
                if status:
                    self._validator.is_status_exists(status)
                    filtered_tasks = list(filter(lambda t: t.status == status, filtered_tasks))
                if group:
                    self._validator.is_group_exists(group)
                    filtered_tasks = list(filter(lambda t: t.group == group, filtered_tasks))

                print("filtered tasks -->")
                for i in filtered_tasks:
                    print(f"""
                        ЗАДАЧА: {i.title}
                        ID: {i.id}
                        СТАТУС: {i.status}
                        ГРУППА: {i.group}
                        """)
                print("--------------")
                logger.info("filter-tasks: SUCCESS")
        except ValidationError as e:
            logger.error("list-task --filter: FAILED")
            print(f"ERROR: {e}")

        key = attrgetter(sort_type)
        sorted_tasks = sorted(filtered_tasks,
                    key=key, reverse=False
            )
        
        print("sorted tasks -->")
        for i in sorted_tasks:
            print(f"""
                        ЗАДАЧА: {i.title}
                        ID: {i.id}
                        СТАТУС: {i.status}
                        ГРУППА: {i.group}
                    """)
        print("--------------")
        logger.info("list-tasks: SUCCESS")
       
    def list_groups(self, sort_type):
        key = attrgetter(sort_type)
        sorted_groups = sorted(self._groups,
                    key=key, reverse=False
            )

        print("sorted groups -->")
        for i in sorted_groups:
            print(f"""
                        ГРУППА: {i.title}
                        ID: {i.id}
                    """)
        print("--------------")
        logger.info("list-groups: SUCCESS")

    def delete_task(self, ids):
        try:
            self._validator.is_task_id_exists(ids)

            for i in ids:
                for j in self._tasks:
                    if j.id == i:
                        self._tasks.remove(j)
                        break
            logger.info("delete-task: SUCCESS")

            self._file_manager.save_data(self._tasks, self._groups,
                                        self._next_task_id,
                                        self._next_group_id
                                        )
        except ValidationError as e:
            logger.error("delete-task: FAILED")
            print(f"ERROR: {e}")

    def delete_group(self, ids):
        try:
            self._validator.is_group_id_exists(ids)

            for i in ids:
                for j in self._groups:
                    if j.id == i:
                        self._groups.remove(j)
                        break
            logger.info("delete-group: success")

            self._file_manager.save_data(self._tasks, self._groups,
                                        self._next_task_id,
                                        self._next_group_id
                                        )
        except ValidationError as e:
            logger.error("delete-group: failed")
            print(f"ERROR: {e}")

    def set_status(self, ids, status):
        try:
            self._validator.is_task_id_exists(ids)

            for i in ids:
                for j in self._tasks:
                    if j.id == i:
                        j.status = status
                        break
            logger.info("set-status: SUCCESS")
            
            self._file_manager.save_data(self._tasks, self._groups,
                                        self._next_task_id,
                                        self._next_group_id
                                        )
        except ValidationError as e:
            logger.error("set-status: FAILED")
            print(f"ERROR: {e}")

    def format_task(self, ids, title, status, group):
        try:
            self._validator.is_task_id_exists(ids)
            self._validator.is_group_exists(group)

            for i in ids:
                for j in self._tasks:
                    if j.id == i:
                        j.title = title
                        j.status = status
                        j.group = group
                        break
            logger.info("format-task: SUCCESS")
            
            self._file_manager.save_data(self._tasks, self._groups,
                                        self._next_task_id,
                                        self._next_group_id
                                        )
        except ValidationError as e:
            logger.error("format-task: FAILED")
            print(f"ERROR: {e}")

    def format_group(self, ids, title):
        try:
            self._validator.is_group_id_exists(ids)
            self._validator.is_group_not_exists(title)

            for i in ids:    
                for g in self._groups:
                    if g.id == i:
                        for t in self._tasks:
                            if t.group == g.title:
                                t.group = title
                        g.title = title

            logger.info("gormat-group: SUCCESS")
            
            self._file_manager.save_data(self._tasks, self._groups,
                                        self._next_task_id,
                                        self._next_group_id
                                        )
        except ValidationError as e:
            logger.error("format-group: FAILED")
            print(f"ERROR: {e}")

