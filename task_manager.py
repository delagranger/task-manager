import logging

from task import Task
from group import Group
from db_manager import DBManager

log = logging.getLogger(__name__)

class TaskManager:
    def __init__(self):
        self._db_manager = DBManager()


    def add_task(self, title, status, group):        
        task = Task(title, status, group)
        self._db_manager.add_task(task)


    def add_group(self, title):
        group = Group(title)
        self._db_manager.add_group(group)
 

    def list_tasks(self, sort_type, status, group, filtered=False):
        rows = self._db_manager.list_tasks(sort_type, status, group, filtered)

        print("listed tasks -->")
        for t in rows:
            Task.print_task(t)
        print("---------------")
        log.info("list-tasks: SUCCESS; sorted by %s, filtered by status=%s and group=%s", 
                 sort_type, status, group,
        )


    def list_groups(self, sort_type):
        rows = self._db_manager.list_groups(sort_type)

        print("listed groups -->")
        for g in rows:
            Group.print_group(g)
        print("---------------")
        log.info("list-groups: SUCCESS; sort type=%s", sort_type)


    def delete_task(self, ids):
        self._db_manager.delete_task(ids)


    def delete_group(self, ids):
        self._db_manager.delete_group(ids)


    def set_status(self, ids, status):
        self._db_manager.set_status(ids, status)  


    def format_task(self, ids, title, status, group):
        self._db_manager.format_task(ids, title, status, group)


    def format_group(self, id, title):
        self._db_manager.format_group(id, title)


