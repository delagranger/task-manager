import logging

log = logging.getLogger(__name__)

class CLIOutput:
    def __init__(self):
        pass

    def display_tasks(self, tasks):
        try:
            print("Displayed tasks -->")
            for t in tasks:
                print(f"ID: {t[0]}; Title: {t[1]}; Status: {t[2]}; Group: {t[3]}")
            print('-' * 19)
            log.debug("Display tasks: SUCCESS")
        except Exception as e:
            log.error("Display tasks: FAILED\nERROR: %s", e)
            raise


    def display_groups(self, groups):
        try:
            print("Displayed groups -->")
            for g in groups:
                print(f"ID: {g[0]}; Title: {g[1]};")
            print('-' * 20)
            log.debug("Display groups: SUCCESS")
        except Exception as e:
            log.error("Display groups: FAILED\nERROR: %s", e)
            raise


    def display_task_created(self, id, title, status, group):
        try:
            print(f"Task created; ID={id}, Title={title}, Status={status}, {group}")
            log.debug("Display task created: SUCCESS")
        except Exception as e:
            log.error("Display task created: FAILED\nERROR: %s", e)
            raise


    def display_group_created(self, id, title):
        try:
            print(f"Group created; ID={id}, Title={title}")
            log.debug("Display group created: SUCCESS")
        except Exception as e:
            log.error("Display group created: FAILED\nERROR: %s", e)
            raise


    def display_tasks_deleted(self, ids):
        try:
            print(f"Tasks deleted; IDs={ids}")
            log.debug("Display tasks deleted: SUCCESS")
        except Exception as e:
            log.error("Display tasks deleted: FAILED\nERROR: %s", e)
            raise


    def display_groups_deleted(self, ids):
        try:
            print(f"Groups deleted; IDs={ids}")
            log.debug("Display groups deleted: SUCCESS")
        except Exception as e:
            log.error("Display groups deleted: FAILED\nERROR: %s", e)
            raise


    def display_status_set(self, ids, status):
        try:
            print(f"Status for tasks {ids} set. New status is {status}")
            log.debug("Display status set: SUCCESS")
        except Exception as e:
            log.error("Display status set: FAILED\nERROR: %s", e)
            raise


    def display_task_formated(self, ids, title, status, group):
        try:
            print(f"Tasks {ids} formated. New title is {title}, new status is {status}, new group is {group}")
            log.debug("Display tasks formated: SUCCESS")
        except Exception as e:
            log.error("Display tasks formated: FAILED\nERROR: %s", e)
            raise


    def display_group_formated(self, id, title):
        try:
            print(f"Group {id} formated. New title is {title}")
            log.debug("Display groups formated: SUCCESS")
        except Exception as e:
            log.error("Display groups formated: FAILED\nERROR: %s", e)
            raise


    def display_incorrect_command(self, command):
        try:
            print(f"Incorrect command! Command {command} is not exists") 
            log.debug("Display incorrect command error: SUCCESS")   
        except Exception as e:
            log.error("Display incorrect command error: FAILED\nERROR: %s", e) 
            raise


    def display_error(self, error: Exception, command):
        try:
            print(f"Unable to {command}, type '-h' for help\nERROR: {error}")
            log.debug("Display error: SUCCESS") 
        except Exception as e:
            log.error("Display error: FAILED\nERROR: %s", e) 
            raise
