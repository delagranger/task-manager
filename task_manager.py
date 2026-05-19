from operator import attrgetter
import logging

from task import Task
from group import Group
from file_manager import FileManager
from validators import Validator, ValidationError

log = logging.getLogger(__name__)

class TaskManager:
    def __init__(self):
        self._file_manager = FileManager()
        self._validator = Validator(self)
        self._next_task_id, self._next_group_id = self._file_manager.load_ids()
        self._tasks = self._file_manager.load_tasks()
        self._groups = self._file_manager.load_groups()

    def add_task(self, title, status, group):
        try:
            self._validator.verify_group_exists(group, expected_exist=True)
            
            task = Task(title, 
                        self._next_task_id,
                        status, group,
            )
            self._next_task_id += 1
            self._tasks.append(task)
            log.info("add-task: SUCCESS; id=%s, title=%s, status=%s, group=%s",
                     task.id, title, status, group
            )

            self._file_manager.save_data(self._tasks, self._groups, 
                                         self._next_task_id, 
                                         self._next_group_id,
            )
        except ValidationError as e:
            log.error("add-task: FAILED")
            log.error("ERROR: %s", e)

    def add_group(self, title):
        try:
            self._validator.verify_group_exists(title, expected_exist=False)

            group = Group(title, self._next_group_id)
            self._next_group_id += 1
            self._groups.append(group)
            log.info("add-group: SUCCESS; id=%s, title=%s", group.id, title)

            self._file_manager.save_data(self._tasks, self._groups, 
                                         self._next_task_id, 
                                         self._next_group_id,
            )
        except ValidationError as e:
            log.error("add-group: FAILED")
            log.error("ERROR: %s", e)

    def list_tasks(self, sort_type, status, group, filtered=False):
        filtered_tasks = self._tasks
        try:
            if filtered:
                if status:
                    self._validator.verify_status_exists(status)
                    filtered_tasks = list(filter(lambda t: t.status == status, 
                                                 filtered_tasks
                    ))
                if group:
                    self._validator.verify_group_exists(group, expected_exist=True)
                    filtered_tasks = list(filter(lambda t: t.group == group, 
                                                 filtered_tasks
                    ))

                print("filtered tasks -->")
                for i in filtered_tasks:
                    print(f"""
                        ЗАДАЧА: {i.title}
                        ID: {i.id}
                        СТАТУС: {i.status}
                        ГРУППА: {i.group}
                        """)
                print("--------------")
                log.info("filter-tasks: SUCCESS; filtered by status=%s and group=%s", status, group)
        except ValidationError as e:
            log.error("list-task --filter: FAILED")
            log.error("ERROR: %s", e)

        key = attrgetter(sort_type)
        sorted_tasks = sorted(filtered_tasks, key=key, reverse=False)
        
        print("sorted tasks -->")
        for i in sorted_tasks:
            print(f"""
                        ЗАДАЧА: {i.title}
                        ID: {i.id}
                        СТАТУС: {i.status}
                        ГРУППА: {i.group}
                    """)
        print("--------------")
        log.info("list-tasks: SUCCESS; sort type=%s", sort_type)

    def list_groups(self, sort_type):
        key = attrgetter(sort_type)
        sorted_groups = sorted(self._groups, key=key, reverse=False)

        print("sorted groups -->")
        for i in sorted_groups:
            print(f"""
                        ГРУППА: {i.title}
                        ID: {i.id}
                    """)
        print("--------------")
        log.info("list-groups: SUCCESS; sort type=%s", sort_type)

    def delete_task(self, ids):
        try:
            self._validator.verify_task_id_exists(ids)

            for i in ids:
                for j in self._tasks:
                    if j.id == i:
                        self._tasks.remove(j)
                        break
            log.info("delete-task: SUCCESS; id=%s", ids)

            self._file_manager.save_data(self._tasks, self._groups, 
                                         self._next_task_id, 
                                         self._next_group_id,
            )
        except ValidationError as e:
            log.error("delete-task: FAILED")
            log.error("ERROR: %s", e)

    def delete_group(self, ids):
        try:
            self._validator.verify_group_id_exists(ids)

            for i in ids:
                for j in self._groups:
                    if j.id == i:
                        self._groups.remove(j)
                        break
            log.info("delete-group: SUCCESS; id=%s", ids)

            self._file_manager.save_data(self._tasks, self._groups, 
                                         self._next_task_id, 
                                         self._next_group_id,
            )
        except ValidationError as e:
            log.error("delete-group: FAILED")
            log.error("ERROR: %s", e)

    def set_status(self, ids, status):
        try:
            self._validator.verify_task_id_exists(ids)

            for i in ids:
                for j in self._tasks:
                    if j.id == i:
                        j.status = status
                        break
            log.info("set-status: SUCCESS; id=%s, new status=%s", ids, status)
            
            self._file_manager.save_data(self._tasks, self._groups, 
                                         self._next_task_id, 
                                         self._next_group_id,
            )
        except ValidationError as e:
            log.error("set-status: FAILED")
            log.error("ERROR: %s", e)

    def format_task(self, ids, title, status, group):
        try:
            self._validator.verify_task_id_exists(ids)
            self._validator.verify_group_exists(group, expected_exist=True)

            for i in ids:
                for j in self._tasks:
                    if j.id == i:
                        j.title = title
                        j.status = status
                        j.group = group
                        break
            log.info("format-task: SUCCESS; id=%s, new title=%s, new status=%s, new group=%s", 
                     ids, title, status, group
            )
            
            self._file_manager.save_data(self._tasks, self._groups, 
                                         self._next_task_id, 
                                         self._next_group_id,
            )
        except ValidationError as e:
            log.error("format-task: FAILED")
            log.error("ERROR: %s", e)

    def format_group(self, id, title):
        try:
            self._validator.verify_group_id_exists(id)
            self._validator.verify_group_exists(title, expected_exist=False)

            for i in id:    
                for g in self._groups:
                    if g.id == i:
                        for t in self._tasks:
                            if t.group == g.title:
                                t.group = title
                        g.title = title

            log.info("format-group: SUCCESS; id=%s, new title=%s", id, title)
            
            self._file_manager.save_data(self._tasks, self._groups, 
                                         self._next_task_id, 
                                         self._next_group_id,
            )
        except ValidationError as e:
            log.error("format-group: FAILED")
            log.error("ERROR: %s", e)

