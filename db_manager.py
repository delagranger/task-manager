from dotenv import load_dotenv
import psycopg2
import os
import logging

from exceptions import (StatusNotFound, GIDNotFound, TIDNotFound, GroupNotFound)

log = logging.getLogger(__name__)

load_dotenv()

class DBManager:
    def __init__(self):
        self._conn = self._create_connection()
        self._create_groups_table()
        self._insert_default_group()
        self._create_tasks_table()

    # DONE
    def _create_connection(self):
        try:
            connection = psycopg2.connect(dbname=os.getenv("DB_NAME"), 
                                        user=os.getenv("DB_USER"), 
                                        password=os.getenv("DB_PASSWORD"),
                                        host=os.getenv("DB_HOST"),
                                        port=os.getenv("DB_PORT"),
            )
            log.debug("Create SQL connection: SUCCESS")
            return connection
        except psycopg2.Error as e:
            log.error("Create SQL connection: FAILED\nERROR: %s", e)
            raise

    # DONE
    def _create_groups_table(self):
        try:
            with self._conn.cursor() as cur:
                query = "CREATE TABLE IF NOT EXISTS groups " \
                        "(id SERIAL PRIMARY KEY, title VARCHAR(50) NOT NULL UNIQUE);"
                cur.execute(query)
                self._conn.commit()
                log.debug("Create groups table: SUCCESS")
        except psycopg2.Error as e:
            log.error("Create groups table: FAILED\nERROR: %s", e)
            self._conn.rollback()
            raise

    # DONE
    def _insert_default_group(self):
        try:
            with self._conn.cursor() as cur:
                query = "INSERT INTO groups (title) SELECT 'default group' " \
                        "WHERE NOT EXISTS " \
                        "(SELECT 1 FROM groups WHERE title = 'default group') " \
                        "RETURNING id, title;"
                cur.execute(query)
                if cur.rowcount:
                    group_id, group_title = cur.fetchone()
                    self._conn.commit()
                    log.debug("Insert default group: SUCCESS; GroupID=%r, GroupTitle=%r", 
                            group_id, group_title,
                    )
        except psycopg2.Error as e:
            log.error("Insert default group: FAILED\nERROR: %s", e)
            self._conn.rollback()
            raise

    # DONE
    def _create_tasks_table(self):
        try:
            with self._conn.cursor() as cur:
                query = "CREATE TABLE IF NOT EXISTS tasks " \
                        "(id SERIAL PRIMARY KEY, " \
                        "title VARCHAR(50) NOT NULL, " \
                        "status task_status NOT NULL " \
                        "CHECK (status IN ('active', 'frozen', 'finished')), " \
                        "group_id INTEGER REFERENCES groups(id) " \
                        "ON DELETE SET NULL);"
                cur.execute(query)
                self._conn.commit()
                log.debug("Create tasks table: SUCCESS")
        except psycopg2.Error as e:
            log.error("Create tasks table: FAILED\nERROR: %s", e)
            self._conn.rollback()
            raise

    # DONE
    def add_task(self, task):
        try:
            group_id, group_title = self._ensure_group_title_exists(task.group)
            with self._conn.cursor() as cur:
                query = "INSERT INTO tasks (title, status, group_id) " \
                        "VALUES (%s, %s, %s) " \
                        "RETURNING id, title, status, group_id;"
                cur.execute(query, (task.title, task.status, group_id,))

                id, title, status, group_id = cur.fetchone()
                self._conn.commit()
                log.info("Add task: SUCCESS; ID=%r, Title=%r, Status=%r, Group=%r", 
                         id, title, status, group_title,
                )
                return id, title, status, group_id, group_title
        except (GroupNotFound, psycopg2.Error) as e:
            log.error("Add task: FAILED; Title=%r, Status=%r, Group=%r\nERROR: %s", 
                      task.title, task.status, task.group, e,
            )
            self._conn.rollback()
            raise

    # DONE
    def add_group(self, group):
        try:
            with self._conn.cursor() as cur:
                query = "INSERT INTO groups (title) " \
                        "VALUES (%s) " \
                        "RETURNING id, title;"
                cur.execute(query, (group.title,))

                id, title = cur.fetchone()
                self._conn.commit()
                log.info("Add group: SUCCESS; ID=%r, Title=%r", 
                         id, title,
                )
                return id, title
        except psycopg2.Error as e:
            log.error("Add group: FAILED; Title=%r\nERROR: %s", 
                      group.title, e,
            )
            self._conn.rollback()
            raise


    def list_tasks(self, sort_type, filtered, status, group):
        try:
            query = "SELECT tasks.id, tasks.title, tasks.status, " \
                    "groups.title AS group_title " \
                    "FROM tasks LEFT JOIN groups " \
                    "ON tasks.group_id = groups.id"
            
            conditions = []
            params = []
            if filtered:

                if status:
                    status = self._ensure_status_exists(status)
                    conditions.append("tasks.status = %s")
                    params.append(status)
                
                if group:
                    group_id = self._ensure_group_title_exists(group)
                    conditions.append("tasks.group_id = %s")
                    params.append(group_id)

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            
            query += f" ORDER BY {sort_type} ASC;"

            with self._conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                log.debug("Collect, sort and filter tasks: SUCCESS; " \
                          "Sort type=%r, filter=%r, status=%r, group=%r", 
                          sort_type, filtered, status, group,
                )
                return rows
        except psycopg2.Error as e:
            log.error("Collect, sort and filter tasks: FAILED; " \
                      "Sort type=%r, filter=%r, status=%r, group=%r\nERROR: %s", 
                      sort_type, filtered, status, group, e,
            )
            self._conn.rollback()
            raise


    def list_groups(self, sort_type):
        try:
            with self._conn.cursor() as cur:
                query = f"SELECT * FROM groups ORDER BY {sort_type} ASC;"
                cur.execute(query)
                groups = cur.fetchall()
                log.debug("Collect and sort groups: SUCCESS; Sort type = %r", 
                          sort_type,
                )
                return groups
        except psycopg2.Error as e:
            log.error("Collect and sort groups: FAILED; Sort type=%r\nERROR: %s", 
                      sort_type, e,
            )
            self._conn.rollback()
            raise

    # DONE
    def delete_task(self, ids):
        try:
            with self._conn.cursor() as cur:
                query = "DELETE FROM tasks WHERE id = ANY(%s);"
                cur.execute(query, (ids,))
                ids = self._ensure_task_id_exists(cur.rowcount, ids)
                self._conn.commit()
                log.info("Delete task: SUCCESS; IDs=%r", ids)
                return ids
        except (TIDNotFound, psycopg2.Error) as e:
            log.error("Delete task: FAILED; IDs=%r\nERROR: %s", 
                      ids, e,
            )
            self._conn.rollback()
            raise

    # DONE
    def delete_group(self, ids):
        try:
            with self._conn.cursor() as cur:
                query = "DELETE FROM groups WHERE id = ANY(%s);"
                cur.execute(query, (ids,))
                ids = self._ensure_group_id_exists(cur.rowcount, ids)
                self._conn.commit()
                log.info("Delete group: SUCCESS; IDs=%r", ids)
                return ids
        except (GIDNotFound, psycopg2.Error) as e:
            log.error("Delete group: FAILED; IDs=%r\nERROR: %s", 
                      ids, e,
            )
            self._conn.rollback()
            raise


    def set_status(self, ids, status):
        try:
            with self._conn.cursor() as cur:
                query = "UPDATE tasks SET status = %s " \
                        "WHERE id = ANY(%s);"
                cur.execute(query, (status, ids))
                ids = self._ensure_task_id_exists(cur.rowcount, ids)
                self._conn.commit()
                log.info("Set status: SUCCESS; IDs=%r, New status=%r", 
                         ids, status,
                )
                return ids, status
        except (TIDNotFound, psycopg2.Error) as e:
            log.error("Set status: FAILED; IDs=%r, Status=%r\nERROR: %s", 
                      ids, status, e,
            )
            self._conn.rollback()
            raise

    
    def format_task(self, ids, title, status, group):
        try:
            group_id = self._ensure_group_title_exists(group)
            with self._conn.cursor() as cur:
                query = "UPDATE tasks SET title = %s, status = %s, " \
                        "group_id = %s " \
                        "WHERE id = ANY(%s);"
                cur.execute(query, (title, status, group_id, ids))
                ids = self._ensure_task_id_exists(cur.rowcount, ids)
                self._conn.commit()
                log.info("Format task: SUCCESS; ID=%r, New title=%r, New status=%r, New group=%r", 
                    ids, title, status, group,
                )
                return ids, title, status, group
        except (GroupNotFound, TIDNotFound, psycopg2.Error) as e:
            log.error("Format task: FAILED; ID=%r, Title=%r, Status=%r, Group=%r\nERROR: %s", 
                      ids, title, status, group, e,
            )
            self._conn.rollback()
            raise


    def format_group(self, ids, title):
        try:
            with self._conn.cursor() as cur:
                query = "UPDATE groups SET title = %s " \
                        "WHERE id = ANY(%s)"
                cur.execute(query, (title, ids))
                ids = self._ensure_group_id_exists(cur.rowcount, ids)
                self._conn.commit()
                log.info("Format group: SUCCESS; ID=%r, New title=%r", 
                         ids, title,
                )
                return ids, title
        except (GIDNotFound, psycopg2.Error) as e:
            log.error("Format group: FAILED; ID=%r, Title=%r\nERROR: %s", 
                      ids, title, e,
            )
            self._conn.rollback()
            raise

    # DONE
    def _ensure_group_title_exists(self, title):
        with self._conn.cursor() as cur:
            query = "SELECT id FROM groups WHERE title = %s;"
            cur.execute(query, (title,))
            row = cur.fetchone()
            if row:
                group_id = row[0]
                log.debug("Ensure groups title exists: SUCCESS; GroupID=%r, GroupTitle=%r",
                          group_id, title,
                )
                return group_id
            else:
                log.error("Ensure groups title exists: FAILED; GroupTitle=%r",
                          title,
                )
                raise GroupNotFound(title)

    # DONE
    def _ensure_group_id_exists(self, changed_rows, ids):
        if changed_rows < len(ids):
            log.error("Ensure GroupID exists: FAILED; IDs=%r", ids)
            raise GIDNotFound(ids)
        else:
            log.debug("Ensure GroupID exists: SUCCESS; IDs=%r", ids)
            return ids

    # DONE
    def _ensure_task_id_exists(self, changed_rows, ids):
        if changed_rows < len(ids):
            log.error("Ensure TaskID exists: FAILED; IDs=%r", ids)
            raise TIDNotFound(ids)
        else:
            log.debug("Ensure TaskID exists: SUCCESS; IDs=%r", ids)
            return ids


    def _ensure_status_exists(self, status):
        with self._conn.cursor() as cur:
            query = "SELECT * FROM tasks WHERE status = %s;"
            cur.execute(query, (status,))
            if cur.rowcount == 0:
                log.error("Ensure status exists: FAILED; Status=%r", 
                          status
                )
                raise StatusNotFound(status)
            else:
                log.debug("Ensure status exists: SUCCESS; Status=%r", 
                          status
                )
                return status
