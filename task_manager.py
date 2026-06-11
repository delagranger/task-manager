import logging

from task import Task
from group import Group
from db_manager import DBManager
from sqlalchemy_orm.orm_manager import ORMManager
from exceptions import (FilterNotExists, SortTypeNotFound, 
                        IncorrectLength, StatusNotFound)

log = logging.getLogger(__name__)

MAX_GROUP_LENGTH = 25
MAX_TASK_LENGTH = 50
STATUSES = ['active', 'frozen', 'finished']
GROUPS_SORT_TYPES = ['id', 'title']
TASKS_SORT_TYPES = ['id', 'title', 'status', 'group_id']

class TaskManager:
    def __init__(self):
        self._orm_manager = ORMManager()
 

    def add_task(self, title, status, group):  
        title, cur_length = self._ensure_title_is_correct("task", title)
        status = self._ensure_status_is_correct(status)    
        task = Task(title, status, group)
        id, title, status, group = self._orm_manager.add_task(task)
        return id, title, status, group


    def add_group(self, title):
        title, cur_length = self._ensure_title_is_correct("group", title)
        group = Group(title)
        id, title = self._orm_manager.add_group(group)
        return id, title


    def list_tasks(self, sort_type, filtered, status, group):
        sort_type = self._ensure_sort_type_is_correct("task", sort_type)
        self._ensure_filter_exists(filtered, status, group)
        tasks = self._orm_manager.list_tasks(sort_type, filtered, status, group)
        return tasks

   
    def list_groups(self, sort_type):
        sort_type = self._ensure_sort_type_is_correct("group", sort_type)
        groups = self._orm_manager.list_groups(sort_type)
        return groups

   
    def delete_task(self, ids):
        ids = self._orm_manager.delete_task(ids)
        return ids


    def delete_group(self, ids):
        ids = self._orm_manager.delete_group(ids)
        return ids

  
    def set_status(self, ids, status):
        status = self._ensure_status_is_correct(status)
        ids, status = self._orm_manager.set_status(ids, status)
        return ids, status


    def format_task(self, ids, title, status, group):
        title, cur_length = self._ensure_title_is_correct("task", title)
        ids, title, status, group = self._orm_manager.format_task(
            ids, title, status, group
        )
        return ids, title, status, group
    

    def format_group(self, id, title):
        title, cur_length = self._ensure_title_is_correct("group", title)
        id, title = self._orm_manager.format_group(id, title)
        return id, title


    def _ensure_sort_type_is_correct(self, obj_type, sort_type):
        if obj_type == "task" and sort_type not in TASKS_SORT_TYPES:
            sort_types = TASKS_SORT_TYPES
            log.error("Ensure sort type is correct: FAILED; Sort type=%r", 
                      sort_type,
            )
            raise SortTypeNotFound(sort_type, sort_types)
        elif obj_type == "group" and sort_type not in GROUPS_SORT_TYPES:
            sort_types = GROUPS_SORT_TYPES
            log.error("Ensure sort type is correct: FAILED; Sort type=%r", 
                      sort_type,
            )
            raise SortTypeNotFound(sort_type, sort_types)
        else:
            log.debug("Ensure sort type is correct: SUCCESS; Sort type=%r", 
                      sort_type,
            )
            return sort_type
    

    def _ensure_filter_exists(self, filtered, status, group):
        if filtered and (status or group):
            log.debug("Ensure filter exists: SUCCESS; Filter=%r, Status=%r, Group=%r", 
                      filtered, status, group,
            )
            return status, group
        elif filtered and not status and not group:
            log.error("Ensure filter exists: FAILED; Filter=%r, Status=%r, Group=%r", 
                      filtered, status, group,
            )
            raise FilterNotExists()
        elif not filtered and (status or group):
            log.error("Ensure filter exists: FAILED; Filter=%r, Status=%r, Group=%r", 
                      filtered, status, group,
            )
            raise FilterNotExists()
        else:
            log.warning("Ensure filter exists: FAILED; Filter=%r, Status=%r, Group=%r", 
                        filtered, status, group,
            )


    def _ensure_title_is_correct(self, obj_type, title):
        cur_length = len(title)
        if obj_type == "group" and len(title) > MAX_GROUP_LENGTH:
            max_length = MAX_GROUP_LENGTH
            log.error("Ensure group title is correct: FAILED; Title=%r, length=%r", 
                      title, cur_length,
            )
            raise IncorrectLength(obj_type, cur_length, max_length)
        elif obj_type == "task" and len(title) > MAX_TASK_LENGTH:
            max_length = MAX_TASK_LENGTH
            log.error("Ensure task title is correct: FAILED; Title=%r, length=%r", 
                      title, cur_length,
            )
            raise IncorrectLength(obj_type, cur_length, max_length)
        else:
            log.debug("Ensure title is correct: SUCCESS; Title=%r, length=%r", 
                      title, cur_length,
            )
            return title, cur_length


    def _ensure_status_is_correct(self, status):
        if status not in STATUSES:
            statuses = STATUSES
            log.error("Ensure status is correct: FAILED; Status=%r", 
                      status,
            )
            raise StatusNotFound(status, statuses)
        else:
            log.debug("Ensure status is correct: SUCCESS; Status=%r", 
                      status,
            )
            return status