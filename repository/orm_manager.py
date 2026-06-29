from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
import logging

from config import build_engine
from repository.models.group_model import GroupModel
from repository.models.task_model import TaskModel
from repository.models.base import Base
from repository.session_context_manager import session_scope
from group import Group
from task import Task

from exceptions import (GIDNotFound, TIDNotFound, GroupNotFound)

log = logging.getLogger(__name__)

class ORMManager:
    def __init__(self):
        self._engine = build_engine()
        Base.metadata.create_all(self._engine)
        self.Session = sessionmaker(bind=self._engine)
        self._create_default_group()


    def _create_default_group(self) -> None:
        with session_scope(self.Session, "Create default group") as session:
            query = session.query(GroupModel)
            result = query.filter(GroupModel.title == "default group").first()
            if not result:
                group_orm = GroupModel(title="default group")
                session.add(group_orm)
                session.flush()
                log.debug("Insert default group: SUCCESS; %r", group_orm)  


    def add_task(self, task: Task) -> tuple[int, str, str, str]:
        with session_scope(self.Session, "Add task") as session:
            found_group = session.query(GroupModel).filter(GroupModel.title == task.group).first()
            if not found_group:
                raise GroupNotFound(task.group)
            task_orm = TaskModel(title=task.title, status=task.status, group = found_group)
            session.add(task_orm)
            session.flush()
            log.info("Add task: SUCCESS; ID=%r, Title=%r, Status=%r, Group=%r", task_orm.id, task_orm.title, task_orm.status, task_orm.group)
            return task_orm.id, task_orm.title, task_orm.status, task_orm.group.title


    def add_group(self, group: Group) -> tuple[int, str]:
        with session_scope(self.Session, "Add group") as session:
            group_orm = GroupModel(title=group.title)
            session.add(group_orm)
            session.flush()
            log.info("Add group: SUCCESS; ID=%r, Title=%r", group_orm.id, group_orm.title)
            return group_orm.id, group_orm.title


    def list_tasks(self, sort_type: str, filtered: bool, status: str, group: str) -> list[Task]:
        sorting_map = {'id' : TaskModel.id, 'title' : TaskModel.title, 'status' : TaskModel.status, 'group_id' : TaskModel.group_id}
        with session_scope(self.Session, "List tasks") as session:
            query = session.query(TaskModel)
            if filtered:
                if status:
                    query = query.filter(TaskModel.status == status)
                if group:
                    found_group = session.query(GroupModel).filter(GroupModel.title == group).first()
                    if not found_group:
                        raise GroupNotFound(group)
                    query = query.filter(TaskModel.group_id == found_group.id)
            query = query.order_by(sorting_map[sort_type])
            query = query.options(joinedload(TaskModel.group))
            rows = query.all()
            log.debug("Collect, sort and filter tasks: SUCCESS; " \
                        "Sort type=%r, filter=%r, status=%r, group=%r", 
                        sort_type, filtered, status, group,
                )
            
            tasks = []
            for t in rows:
                task = Task(t.title, t.status, t.group.title, t.id)
                tasks.append(task)
            return tasks


    def list_groups(self, sort_type: str) -> list[Group]:
        sorting_map = {'id' : GroupModel.id, 'title' : GroupModel.title}
        with session_scope(self.Session, "List groups") as session:
            query = session.query(GroupModel)
            query = query.order_by(sorting_map[sort_type])
            query = query.options(joinedload(GroupModel.tasks))
            rows = query.all()
            log.debug("Collect and sort groups: SUCCESS; Sort type = %r", 
                        sort_type,
            )

            groups = []
            for g in rows:
                related_tasks=[t.title for t in g.tasks]
                group = Group(g.title, g.id, related_tasks)
                groups.append(group)
            return groups


    def delete_task(self, ids: list[int]) -> list[int]:
        with session_scope(self.Session, "Delete task") as session:
            query = session.query(TaskModel)
            tasks = query.filter(TaskModel.id.in_(ids)).all()
            if len(tasks) < len(ids):
                raise TIDNotFound(ids)

            for task in tasks:
                session.delete(task)
            log.info("Delete task: SUCCESS; IDs=%r", ids)
            return ids


    def delete_group(self, id: list[int]) -> list[int]:
        with session_scope(self.Session, "Delete group") as session:
            query = session.query(GroupModel)
            groups = query.filter(GroupModel.id.in_(id)).all()
            if len(groups) < len(id):
                raise GIDNotFound(id)
            
            for group in groups:
                session.delete(group)
            log.info("Delete group: SUCCESS; IDs=%r", id)
            return id


    def set_status(self, ids: list[int], status: str) -> tuple[list[int], str]:
        with session_scope(self.Session, "Set status") as session:
            query = session.query(TaskModel)
            tasks = query.filter(TaskModel.id.in_(ids)).all()
            if len(tasks) < len(ids):
                raise TIDNotFound(ids)
            for t in tasks:
                t.status = status
            log.info("Set status: SUCCESS; IDs=%r, New status=%r", ids, status)
            return ids, status


    def format_task(self, ids: list[int], title: str, status: str, group: str) -> tuple[list[int], str, str, str]:
        with session_scope(self.Session, "Format task") as session:
            query = session.query(TaskModel)
            found_group = session.query(GroupModel).filter(GroupModel.title == group).first()
            if not found_group:
                raise GroupNotFound(group)
            tasks = query.filter(TaskModel.id.in_(ids)).all()
            if len(tasks) < len(ids):
                raise TIDNotFound(ids)
            for t in tasks:
                t.title = title
                t.status = status
                t.group = found_group
            log.info("Format task: SUCCESS; ID=%r, New title=%r, New status=%r, New group=%r", ids, title, status, found_group.title)
            return ids, title, status, found_group.title


    def format_group(self, id: list[int], title: str) -> tuple[list[int], str]:
        with session_scope(self.Session, "Format group") as session:
            query = session.query(GroupModel)
            group = query.filter(GroupModel.id.in_(id)).first()
            if len(group) < len(id):
                raise GIDNotFound(id)
            group.title = title
            log.info("Format group: SUCCESS; ID=%r, New title=%r", id, title)
            return id, group.title
