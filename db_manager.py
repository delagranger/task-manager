from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error as SQLError
import os
import sys
import logging


from db_validator import *

log = logging.getLogger(__name__)

load_dotenv()

class DBManager:
    def __init__(self):
        self.conn = self._create_connection()
        self._db_validator = DBValidator(self.conn)
        self._create_tables()
        self._insert_default_group()
    

    def _create_connection(self): # возвращает объект Соединения с postgreSQL
        try:
            connection = psycopg2.connect(dbname=os.getenv("DB_NAME"),
                                        user=os.getenv("DB_USER"),
                                        password=os.getenv("DB_PASSWORD"),
                                        host=os.getenv("DB_HOST"),
                                        port=os.getenv("DB_PORT"),
            )
            return connection
        except SQLError as e:
            log.critical("create DB connection: FAILED")
            log.critical("ERROR: %s", e)
            sys.exit(1)


    def _create_tables(self):
        try:
            with self.conn.cursor() as cur: # создает объект курсора; курсор - инструмент для выполнения SQL-запросов
                # метод, отправляющий и исполняющий SQL-запрос в БД
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS groups (
                                id SERIAL PRIMARY KEY,
                                title VARCHAR(50) NOT NULL UNIQUE
                            );
                            CREATE TABLE IF NOT EXISTS tasks (
                                id SERIAL PRIMARY KEY,
                                title VARCHAR(50) NOT NULL,
                                status VARCHAR(25) NOT NULL,
                                group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
                            );
                """)
                self.conn.commit() # фиксация изменений в БД
        except SQLError as e:
            log.critical("create DB tables: FAILED")
            log.critical("ERROR: %s", e)
            sys.exit(1)


    def _insert_default_group(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO groups (title) 
                            SELECT 'default group'
                            WHERE NOT EXISTS (SELECT 1 FROM groups WHERE title = 'default group');
                """)
                self.conn.commit()
        except SQLError as e:
            log.critical("insert default group: FAILED")
            log.critical("ERROR: %s", e)
            sys.exit(1)


    def add_task(self, task):
        try:
            group_id = self._db_validator.verify_group_exists(task.group)

            with self.conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO tasks (title, status, group_id)
                            VALUES (%s, %s, %s)
                            RETURNING id;
                """, (task.title, task.status, group_id))
                self.conn.commit()
  
                task_id = cur.fetchone()[0]
                log.info("add-task: SUCCESS; id=%s, title=%s, status=%s, group=%s", 
                         task_id, task.title, task.status, task.group
                )
        except (GroupNotFound, SQLError) as e:
            log.error("add-task: FAILED")
            log.error("ERROR: %s", e)
    

    def add_group(self, group):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO groups
                            (title)
                            VALUES (%s)
                            RETURNING id;
                """, (group.title,))
                self.conn.commit()

                group_id = cur.fetchone()[0]
                log.info("add-group: SUCCESS; id=%s, title=%s", 
                         group_id, group.title
                )
        except SQLError as e:
            log.error("add-group: FAILED")
            log.error("ERROR: %s", e)


    def list_tasks(self, sort_type, status, group, filtered):
        try:
            self._db_validator.verify_sort_type_exists(sort_type)
            self._db_validator.verify_filter_exists(status, group, filtered)
            self._db_validator.verify_status_exists(status)

            query = """SELECT tasks.id, tasks.title, tasks.status, 
                    groups.title AS group_title FROM tasks
                    LEFT JOIN groups ON tasks.group_id = groups.id
            """
            query_add = ''

            if status:
                if group:
                    group_id = self._db_validator.verify_group_exists(group)
                    query_add = f"""
                            WHERE status = '{status}'
                            AND group_id = '{group_id}'
                    """
                else:
                    query_add = f"""
                            WHERE status = '{status}'
                    """
            elif group:
                group_id = self._db_validator.verify_group_exists(group)
                query_add = f"""
                        WHERE group_id = '{group_id}'
                """
            else:
                log.info("filter tasks: FAILED")
            
            query += query_add + f" ORDER BY {sort_type} ASC;"

            with self.conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return rows
        except (SortTypeNotFound, FilterNotExists, StatusNotFound, GroupNotFound, SQLError) as e:
            log.error("list-tasks: FAILED; sort type %s, filter status=%s and group=%s", 
                 sort_type, status, group,
            )
            log.error("ERROR: %s", e)
            sys.exit(1)


    def list_groups(self, sort_type):
        try:
            self._db_validator.verify_sort_type_exists(sort_type)

            with self.conn.cursor() as cur:
                query = f"""
                        SELECT * FROM groups
                        ORDER BY {sort_type} ASC;
                """
                cur.execute(query)
                rows = cur.fetchall()
                return rows
        except (SortTypeNotFound, SQLError) as e:
            log.error("list-groups: FAILED; sort type=%s", sort_type)
            log.error("ERROR: %s", e)
            sys.exit(1)


    def delete_task(self, ids):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            DELETE FROM tasks
                            WHERE id = ANY(%s);
                    """, (ids,))
                self._db_validator.verify_task_id_exists(cur.rowcount, ids)
                self.conn.commit()
                log.info("delete-task: SUCCESS; id=%s", ids)
        except (TIDNotFound, SQLError) as e:
            log.error("delete-task: FAILED; id=%s", ids)
            log.error("ERROR: %s", e)


    def delete_group(self, ids):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            DELETE FROM groups
                            WHERE id = ANY(%s);
                    """, (ids,))
                self._db_validator.verify_group_id_exists(cur.rowcount, ids)
                self.conn.commit()
                log.info("delete-group: SUCCESS; id=%s", ids)
        except (GIDNotFound, SQLError) as e:
            log.error("delete-group: FAILED; id=%s", ids)
            log.error("ERROR: %s", e)


    def set_status(self, ids, status):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            UPDATE tasks SET status = %s
                            WHERE id = ANY(%s);
                """, (status, ids))
                self._db_validator.verify_task_id_exists(cur.rowcount, ids)
                self.conn.commit()
                log.info("set-status: SUCCESS; id=%s, new status=%s",
                    ids, status,
                )
        except (TIDNotFound, SQLError) as e:
            log.error("set-status: FAILED; id=%s, status=%s", 
                      ids, status, 
            )
            log.error("ERROR: %s", e)


    def format_task(self, ids, title, status, group):
        try:
            group_id = self._db_validator.verify_group_exists(group)

            with self.conn.cursor() as cur:
                cur.execute("""
                            UPDATE tasks
                            SET title = %s, status = %s, group_id = %s
                            WHERE id = ANY(%s);
                """, (title, status, group_id, ids))
                self._db_validator.verify_task_id_exists(cur.rowcount, ids)
                self.conn.commit()
                log.info("format-task: SUCCESS; id=%s, new title=%s, new status=%s, new group=%s", 
                    ids, title, status, group,
                )
        except (GroupNotFound, TIDNotFound, StatusNotFound, SQLError) as e:
            log.error("format-task: FAILED; id=%s, title=%s, statis=%s, group=%s", 
                      ids, title, status, group
            )
            log.error("ERROR: %s", e)

  
    def format_group(self, id, title):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            UPDATE groups
                            SET title = %s
                            WHERE id = ANY(%s)
                    """, (title, id))
                self._db_validator.verify_group_id_exists(cur.rowcount, id)
                self.conn.commit()
                log.info("format-group: SUCCESS; id=%s, new title=%s", id, title)
        except (GIDNotFound, SQLError) as e:
            log.error("format-group: FAILED; id=%s, title=%s", id, title)
            log.error("ERROR: %s", e)