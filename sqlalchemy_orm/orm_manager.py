from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
import logging

from config import create_orm_engine
from sqlalchemy_orm.orm_models import Base, GroupORM, TaskORM
from exceptions import (StatusNotFound, GIDNotFound, TIDNotFound, GroupNotFound)

log = logging.getLogger(__name__)

class ORMManager:
    def __init__(self):
        try:
            self._engine = create_orm_engine()
            Base.metadata.create_all(self._engine)
            self._Session = sessionmaker(bind=self._engine)
        except SQLAlchemyError as e:
            log.error
        else:
            self._create_default_group()


    def _create_default_group(self):
        try:
            session = self._Session()
            query = session.query(GroupORM)
            result = query.filter(GroupORM.title == "default group").first()
            if not result:
                group_orm = GroupORM(title="default group")
                session.add(group_orm)
                session.commit()
                log.debug("Insert default group: SUCCESS; %r", group_orm)
        except SQLAlchemyError as e:
            session.rollback()
            log.error("Create default group: FAILED\nERROR: %s", e)
            raise


    def add_task(self, task):
        try:
            with self._Session() as session:
                group = self._ensure_group_title_exists(session, task.group)
                task_orm = TaskORM(title=task.title, status=task.status, group = group)
                session.add(task_orm)
                session.commit()
                log.info("Add task: SUCCESS; ID=%r, Title=%r, Status=%r, Group=%r", task_orm.id, task_orm.title, task_orm.status, task_orm.group)
                return task_orm.id, task_orm.title, task_orm.status, task_orm.group
        except SQLAlchemyError as e:
            log.error("Add task: FAILED; Title=%r, Status=%r, Group=%r\nERROR: %s", task.title, task.status, task.group, e)
            session.rollback()
            raise


    def add_group(self, group):
        try:
            with self._Session() as session:
                group_orm = GroupORM(title=group.title)
                session.add(group_orm)
                session.commit()
                log.info("Add group: SUCCESS; ID=%r, Title=%r", group_orm.id, group_orm.title)
                return group_orm.id, group_orm.title
        except SQLAlchemyError as e:
            log.error("Add group: FAILED; Title=%r\nERROR: %s", group.title, e)
            session.rollback()
            raise


    def list_tasks(self, sort_type, filtered, status, group):
        try:
            sorting_map = {'id' : TaskORM.id, 'title' : TaskORM.title, 'status' : TaskORM.status, 'group_id' : TaskORM.group_id}
            with self._Session() as session:
                query = session.query(TaskORM)
                if filtered:
                    if status:
                        status = self._ensure_status_exists(query, status)
                        query = query.filter(TaskORM.status == status)
                    if group:
                        group = self._ensure_group_title_exists(session, group)
                        query = query.filter(TaskORM.group_id == group.id)
                query = query.order_by(sorting_map[sort_type])
                query = query.options(joinedload(TaskORM.group))
                log.debug("Collect, sort and filter tasks: SUCCESS; " \
                            "Sort type=%r, filter=%r, status=%r, group=%r", 
                            sort_type, filtered, status, group,
                    )
                return query.all()
        except (StatusNotFound, GroupNotFound, SQLAlchemyError) as e:
            log.error("Collect, sort and filter tasks: FAILED; " \
                      "Sort type=%r, filter=%r, status=%r, group=%r\nERROR: %s", 
                      sort_type, filtered, status, group, e,
            )
            session.rollback()
            raise


    def delete_task(self, ids):
        try:
            with self._Session() as session:
                query = session.query(TaskORM)
                ids = self._ensure_task_id_exists(query, ids)
                for id in ids:
                    task = query.filter(TaskORM.id == id).first()
                    session.delete(task)
                    session.commit()
                log.info("Delete task: SUCCESS; IDs=%r", ids)
                return ids
        except (TIDNotFound, SQLAlchemyError) as e:
            log.error("Delete task: FAILED; IDs=%r\nERROR: %s", ids, e)
            session.rollback()
            raise
    

    def delete_group(self, ids):
        try:
            with self._Session() as session:
                query = session.query(GroupORM)
                ids = self._ensure_group_id_exists(query, ids)
                for id in ids:
                    group = query.filter(GroupORM.id == id).first()
                    session.delete(group)
                    session.commit()
                log.info("Delete group: SUCCESS; IDs=%r", ids)
                return ids
        except (GIDNotFound, SQLAlchemyError) as e:
            log.error("Delete group: FAILED; IDs=%r\nERROR: %s", ids, e)
            session.rollback()
            raise


    def _ensure_group_title_exists(self, session, title):
        query = session.query(GroupORM)
        group = query.filter(GroupORM.title == title).first()
        if group:
            log.debug("Ensure groups title exists: SUCCESS; GroupID=%r, GroupTitle=%r", group.id, group.title)
            return group
        else:
            log.error("Ensure groups title exists: FAILED; GroupTitle=%r", title)
            raise GroupNotFound(title)
    

    def _ensure_task_id_exists(self, query, ids):
        found_ids = query.filter(TaskORM.id.in_(ids)).all()
        if len(found_ids) < len(ids):
            log.error("Ensure TaskID exists: FAILED; IDs=%r", ids)
            raise TIDNotFound(ids)
        else:
            log.debug("Ensure TaskID exists: SUCCESS; IDs=%r", ids)
            return ids
    

    def _ensure_group_id_exists(self, query, ids):
        found_ids = query.filter(GroupORM.id.in_(ids)).all()
        if len(found_ids) < len(ids):
            log.error("Ensure GroupID exists: FAILED; IDs=%r", ids)
            raise GIDNotFound(ids)
        else:
            log.debug("Ensure GroupID exists: SUCCESS; IDs=%r", ids)
            return ids
    

    def _ensure_status_exists(self, query, status):
        exists = query.filter(TaskORM.status == status).first()
        if exists:
            log.debug("Ensure status exists: SUCCESS; Status=%r", status)
            return status
        else:
            log.error("Ensure status exists: FAILED; Status=%r", status)
            raise StatusNotFound(status)
    
