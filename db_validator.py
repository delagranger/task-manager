import logging

from exceptions import *

log = logging.getLogger(__name__)

class DBValidator:
    def __init__(self, conn):
        self._conn = conn


    def verify_group_exists(self, title):
        with self._conn.cursor() as cur:
            cur.execute("""
                        SELECT id FROM groups 
                        WHERE title = %s;
            """, (title,))
            row = cur.fetchone()
            if row:
                group_id = row[0]
                log.debug("verify group exists: SUCCESS; id=%s, title=%s",
                          group_id, title,
                )
                return group_id
            else:
                log.error("verify group exists: FAILED; title=%s",
                          title,
                )
                raise GroupNotFound(title)
    

    def verify_group_id_exists(self, changed_rows, ids):
        if changed_rows == 0:
            log.error("verify group id exists: FAILED")
            raise GIDNotFound(ids)
        else:
            log.debug("verify group id exists: SUCCESS")
        
    
    def verify_task_id_exists(self, changed_rows, ids):
        if changed_rows < len(ids):
            log.error("verify task id exists: FAILED")
            raise TIDNotFound(ids)
        else:
            log.debug("verify task id exists: SUCCESS")


    def verify_status_exists(self, status):
        with self._conn.cursor() as cur:
            cur.execute("""
                        SELECT * FROM tasks
                        WHERE status = %s;
            """, (status,))
            if cur.rowcount == 0:
                log.error("verify status exists: FAILED")
                raise StatusNotFound(status)
            else:
                log.debug("verify status exists: SUCCESS")
    

    def verify_sort_type_exists(self, sort_type):
        sort_types = ["id", "title", "status", "group"]
        if sort_type not in sort_types:
            log.error("verify sort type exists: FAILED")
            raise SortTypeNotFound(sort_type)
        else:
            log.debug("verify sort type exists: SUCCESS")
        
    
    def verify_filter_exists(self, status, group, filtered):
        if filtered and not status and not group:
            log.error("verify filter exists: FAILED")
            raise FilterNotExists()
        elif status or group:
            log.debug("verify filter exists: SUCCESS")
       