from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Query
from sqlalchemy.orm import joinedload
import logging

from config import build_engine
from repository.models.group_model import GroupModel
from repository.models.task_model import TaskModel
from repository.models.base import Base
from repository.session_context_manager import session_scope
from group import Group
from task import Task

from exceptions import (StatusNotFound, GIDNotFound, TIDNotFound, GroupNotFound)

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
            group = self._ensure_group_title_exists(session, task.group)
            task_orm = TaskModel(title=task.title, status=task.status, group = group)
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
                    status = self._ensure_status_exists(query, status)
                    query = query.filter(TaskModel.status == status)
                if group:
                    group = self._ensure_group_title_exists(session, group)
                    query = query.filter(TaskModel.group_id == group.id)
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
            ids = self._ensure_task_id_exists(query, ids)
            for id in ids:
                task = query.filter(TaskModel.id == id).first()
                session.delete(task)
            log.info("Delete task: SUCCESS; IDs=%r", ids)
            return ids


    def delete_group(self, id: list[int]) -> list[int]:
        with session_scope(self.Session, "Delete group") as session:
            query = session.query(GroupModel)
            id = self._ensure_group_id_exists(query, id)
            for id in id:
                group = query.filter(GroupModel.id == id).first()
                session.delete(group)
            log.info("Delete group: SUCCESS; IDs=%r", id)
            return id


    def set_status(self, ids: list[int], status: str) -> tuple[list[int], str]:
        with session_scope(self.Session, "Set status") as session:
            query = session.query(TaskModel)
            ids = self._ensure_task_id_exists(query, ids)
            tasks = query.filter(TaskModel.id.in_(ids)).all()
            for t in tasks:
                t.status = status
            log.info("Set status: SUCCESS; IDs=%r, New status=%r", ids, status)
            return ids, status


    def format_task(self, ids: list[int], title: str, status: str, group: str) -> tuple[list[int], str, str, str]:
        with session_scope(self.Session, "Format task") as session:
            query = session.query(TaskModel)
            group = self._ensure_group_title_exists(session, group)
            ids = self._ensure_task_id_exists(query, ids)
            tasks = query.filter(TaskModel.id.in_(ids)).all()
            for t in tasks:
                t.title = title
                t.status = status
                t.group = group
            log.info("Format task: SUCCESS; ID=%r, New title=%r, New status=%r, New group=%r", ids, title, status, group)
            return ids, title, status, group.title


    def format_group(self, id: list[int], title: str) -> tuple[list[int], str]:
        with session_scope(self.Session, "Format group") as session:
            query = session.query(GroupModel)
            id = self._ensure_group_id_exists(query, id)
            group = query.filter(GroupModel.id.in_(id)).first()
            group.title = title
            log.info("Format group: SUCCESS; ID=%r, New title=%r", id, title)
            return id, group.title


    def _ensure_group_title_exists(self, session: Session, title: str) -> GroupModel:
        query = session.query(GroupModel)
        group = query.filter(GroupModel.title == title).first()
        if group:
            log.debug("Ensure groups title exists: SUCCESS; GroupID=%r, GroupTitle=%r", group.id, group.title)
            return group
        else:
            log.error("Ensure groups title exists: FAILED; GroupTitle=%r", title)
            raise GroupNotFound(title)


    def _ensure_task_id_exists(self, query: Query[TaskModel], ids: list[int]) -> list[int]:
        found_ids = query.filter(TaskModel.id.in_(ids)).all()
        if len(found_ids) < len(ids):
            log.error("Ensure TaskID exists: FAILED; IDs=%r", ids)
            raise TIDNotFound(ids)
        else:
            log.debug("Ensure TaskID exists: SUCCESS; IDs=%r", ids)
            return ids


    def _ensure_group_id_exists(self, query: Query[GroupModel], id: list[int]) -> list[int]:
        found_ids = query.filter(GroupModel.id.in_(id)).all()
        if len(found_ids) < len(id):
            log.error("Ensure GroupID exists: FAILED; IDs=%r", id)
            raise GIDNotFound(id)
        else:
            log.debug("Ensure GroupID exists: SUCCESS; IDs=%r", id)
            return id


    def _ensure_status_exists(self, query: Query[TaskModel], status: str) -> str:
        exists = query.filter(TaskModel.status == status).first()
        if exists:
            log.debug("Ensure status exists: SUCCESS; Status=%r", status)
            return status
        else:
            log.error("Ensure status exists: FAILED; Status=%r", status)
            raise StatusNotFound(status)
    