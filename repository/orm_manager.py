from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
import logging

from config import build_engine
from .models import GroupModel, TaskModel, Base
from .session_context_manager import session_scope
from domain import Group, Task

from exceptions import GIDNotFound, TIDNotFound, GroupNotFound, GroupAlreadyExists

log = logging.getLogger(__name__)

class ORMManager:
    def __init__(self):
        self._engine = build_engine()
        Base.metadata.create_all(self._engine)
        self.Session = sessionmaker(bind=self._engine)
        self._create_default_group()


    def _create_default_group(self) -> None:
        with session_scope(self.Session) as session:
            query = session.query(GroupModel)
            result = query.filter(GroupModel.title == "default group").first()
            if not result:
                group_orm = GroupModel(title="default group")
                session.add(group_orm)
                session.flush()
                log.debug("Insert default group: SUCCESS; %r", group_orm)  


    def add_task(self, task: Task) -> tuple[int, str, str, str]:
        with session_scope(self.Session) as session:
            found_group = session.query(GroupModel).filter(GroupModel.title == task.group).first()
            if not found_group:
                raise GroupNotFound(task.group)
            else:
                task_orm = TaskModel(title=task.title, status=task.status, group = found_group)
                session.add(task_orm)
            session.flush()
            log.info("Add task: SUCCESS; ID=%r, Title=%r, Status=%r, Group=%r", task_orm.id, task_orm.title, task_orm.status, task_orm.group)
            return task_orm.id, task_orm.title, task_orm.status, task_orm.group.title


    def add_group(self, group: Group) -> tuple[int, str]:
        with session_scope(self.Session) as session:
            query = session.query(GroupModel)
            existing_group = query.filter(GroupModel.title == group.title).first()
            if existing_group:
                raise GroupAlreadyExists(group.title)
            else:
                group_orm = GroupModel(title=group.title)
                session.add(group_orm)
                session.flush()
                log.info("Add group: SUCCESS; ID=%r, Title=%r", group_orm.id, group_orm.title)
                return group_orm.id, group_orm.title


    def list_tasks(self, sort_type: str, filtered: bool, status: str, group: str) -> list[Task]:
        print("ORM list_tasks entered")
        sorting_map = {'id' : TaskModel.id, 'title' : TaskModel.title, 'status' : TaskModel.status, 'group_id' : TaskModel.group_id}
        with session_scope(self.Session) as session:
            query = session.query(TaskModel)
            if filtered:
                if status:
                    query = query.filter(TaskModel.status == status)
                if group:
                    found_group = session.query(GroupModel).filter(GroupModel.title == group).first()
                    if not found_group:
                        raise GroupNotFound(group)
                    else:
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
        with session_scope(self.Session) as session:
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


    def delete_task(self, id: int) -> int:
        with session_scope(self.Session) as session:
            query = session.query(TaskModel)
            task = query.filter(TaskModel.id == id).first()
            if not task:
                raise TIDNotFound(id)
            else:
                session.delete(task)
        log.info("Delete task: SUCCESS; ID=%r", id)
        return id


    def delete_group(self, id: int) -> int:
        with session_scope(self.Session) as session:
            query = session.query(GroupModel)
            group = query.filter(GroupModel.id == id).first()
            if not group:
                raise GIDNotFound(id)
            else:
                default_group = query.filter(GroupModel.title == "default group").first()
                for task in group.tasks:
                    task.group = default_group
                    
                session.delete(group)
        log.info("Delete group: SUCCESS; ID=%r", id)
        return id


    def patch_task(self, id: int, title: str | None, status: str | None, group: str | None) -> tuple[int, str | None, str | None, str | None]:
        with session_scope(self.Session) as session:
            query = session.query(TaskModel)
            task = query.filter(TaskModel.id == id).first()
            if not task:
                raise TIDNotFound(id)
            if title is not None:
                task.title = title
            if status is not None:
                task.status = status
            if group is not None:
                found_group = session.query(GroupModel).filter(GroupModel.title == group).first()
                if not found_group:
                    raise GroupNotFound(group)
                task.group = found_group
            new_task = task.id, task.title, task.status, task.group.title
        log.info("Format task: SUCCESS; ID=%r, New title=%r, New status=%r, New group=%r", new_task[0], new_task[1], new_task[2], new_task[3])
        return new_task


    def patch_group(self, id: int, title: str | None) -> tuple[int, str | None]:
        with session_scope(self.Session) as session:
            query = session.query(GroupModel)
            group = query.filter(GroupModel.id == id).first()
            if not group:
                raise GIDNotFound(id)
            if title is not None:
                existing_group = query.filter(GroupModel.title == title).first()
                if existing_group:
                    raise GroupAlreadyExists(existing_group.title)
                else:
                    group.title = title
                    new_group = group.id, group.title
        log.info("Format group: SUCCESS; ID=%r, New title=%r", new_group[0], new_group[1])
        return new_group
