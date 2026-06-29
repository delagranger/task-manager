import logging
from task import Task
from group import Group

log = logging.getLogger(__name__)

class CLIOutput:
    def __init__(self):
        pass


    def display_tasks(self, tasks: list[Task]) -> None:
        print("Displayed tasks -->")
        for t in tasks:
            print(f"Task\nID: {t.id}; Title: {t.title}; Status: {t.status}; Group: {t.group}")
        print('-' * 19)


    def display_groups(self, groups: list[Group]) -> None:
        print("Displayed groups -->")
        print('-' * 20)
        for g in groups:
            print(f"Group\nID: {g.id}; Title: {g.title};")
            for t in g.tasks:
                print(f"Task: {t}")
            print('-' * 20)


    def display_task_created(self, id: int, title: str, status: str, group: str) -> None:
        print(f"Task created; ID={id}, Title={title}, Status={status}, Group={group}")


    def display_group_created(self, id: int, title: str) -> None:
        print(f"Group created; ID={id}, Title={title}")


    def display_tasks_deleted(self, ids: list[int]) -> None:
        print(f"Tasks deleted; IDs={ids}")


    def display_groups_deleted(self, ids: list[int]) -> None:
        print(f"Groups deleted; IDs={ids}")


    def display_status_set(self, ids: list[int], status: str) -> None:
        print(f"Status for tasks {ids} set. New status is {status}")
           

    def display_task_formated(self, ids: list[int], title: str, status: str, group: str) -> None:
        print(f"Tasks {ids} formated. New title is {title}, new status is {status}, new group is {group}")


    def display_group_formated(self, id: int, title: str) -> None:
        print(f"Group {id} formated. New title is {title}")


    def display_incorrect_command(self, command: str) -> None:
        print(f"Incorrect command! Command {command} is not exists") 


    def display_error(self, error: BaseException, command: str) -> None:
        print(f"Unable to {command}, type '-h' for help\nERROR: {error}")
