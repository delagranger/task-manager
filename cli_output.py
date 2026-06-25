import logging
from task import Task
from group import Group

log = logging.getLogger(__name__)

class CLIOutput:
    def __init__(self):
        pass


    def display_tasks(self, tasks: list[Task]) -> None:
        try:
            print("Displayed tasks -->")
            for t in tasks:
                print(f"Task\nID: {t.id}; Title: {t.title}; Status: {t.status}; Group: {t.group}")
            print('-' * 19)
            log.debug("Display tasks: SUCCESS")
        except Exception as e:
            log.error("Display tasks: FAILED\nERROR: %s", e)
            raise


    def display_groups(self, groups: list[Group]) -> None:
        try:
            print("Displayed groups -->")
            print('-' * 20)
            for g in groups:
                print(f"Group\nID: {g.id}; Title: {g.title};")
                for t in g.tasks:
                    print(f"Task: {t}")
                print('-' * 20)
            log.debug("Display groups: SUCCESS")
        except Exception as e:
            log.error("Display groups: FAILED\nERROR: %s", e)
            raise


    def display_task_created(self, id: int, title: str, status: str, group: str) -> None:
        try:
            print(f"Task created; ID={id}, Title={title}, Status={status}, Group={group}")
            log.debug("Display task created: SUCCESS")
        except Exception as e:
            log.error("Display task created: FAILED\nERROR: %s", e)
            raise


    def display_group_created(self, id: int, title: str) -> None:
        try:
            print(f"Group created; ID={id}, Title={title}")
            log.debug("Display group created: SUCCESS")
        except Exception as e:
            log.error("Display group created: FAILED\nERROR: %s", e)
            raise


    def display_tasks_deleted(self, ids: list[int]) -> None:
        try:
            print(f"Tasks deleted; IDs={ids}")
            log.debug("Display tasks deleted: SUCCESS")
        except Exception as e:
            log.error("Display tasks deleted: FAILED\nERROR: %s", e)
            raise


    def display_groups_deleted(self, ids: list[int]) -> None:
        try:
            print(f"Groups deleted; IDs={ids}")
            log.debug("Display groups deleted: SUCCESS")
        except Exception as e:
            log.error("Display groups deleted: FAILED\nERROR: %s", e)
            raise


    def display_status_set(self, ids: list[int], status: str) -> None:
        try:
            print(f"Status for tasks {ids} set. New status is {status}")
            log.debug("Display status set: SUCCESS")
        except Exception as e:
            log.error("Display status set: FAILED\nERROR: %s", e)
            raise


    def display_task_formated(self, ids: list[int], title: str, status: str, group: str) -> None:
        try:
            print(f"Tasks {ids} formated. New title is {title}, new status is {status}, new group is {group}")
            log.debug("Display tasks formated: SUCCESS")
        except Exception as e:
            log.error("Display tasks formated: FAILED\nERROR: %s", e)
            raise


    def display_group_formated(self, id: int, title: str) -> None:
        try:
            print(f"Group {id} formated. New title is {title}")
            log.debug("Display groups formated: SUCCESS")
        except Exception as e:
            log.error("Display groups formated: FAILED\nERROR: %s", e)
            raise


    def display_incorrect_command(self, command: str) -> None:
        try:
            print(f"Incorrect command! Command {command} is not exists") 
            log.debug("Display incorrect command error: SUCCESS")   
        except Exception as e:
            log.error("Display incorrect command error: FAILED\nERROR: %s", e) 
            raise


    def display_error(self, error: BaseException, command: str) -> None:
        try:
            print(f"Unable to {command}, type '-h' for help\nERROR: {error}")
            log.debug("Display error: SUCCESS") 
        except Exception as e:
            log.error("Display error: FAILED\nERROR: %s", e) 
            raise
