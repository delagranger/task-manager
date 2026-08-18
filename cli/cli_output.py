import logging
import traceback
from domain import Task, Group

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


    def display_tasks_deleted(self, id: int) -> None:
        print(f"Task deleted; ID={id}")


    def display_groups_deleted(self, id: int) -> None:
        print(f"Group deleted; ID={id}")
           

    def display_task_formated(self, ids: list[int], title: str, status: str, group: str) -> None:
        print(f"Tasks {ids} formated. New title is {title}, new status is {status}, new group is {group}")


    def display_group_formated(self, id: int, title: str) -> None:
        print(f"Group {id} formated. New title is {title}")


    def display_incorrect_command(self, command: str) -> None:
        print(f"Incorrect command! Command {command} is not exists") 


    def display_help(self) -> None:
        print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                     TASK MANAGER CLI                     ║
    ╚══════════════════════════════════════════════════════════╝

    Usage: python main_cli.py <command> [options]

    Commands:
      add-task       Создать новую задачу
      add-group      Создать новую группу
      list-tasks     Показать все задачи
      list-groups    Показать все группы
      delete-task    Удалить задачу(и) по ID
      delete-group   Удалить группу(ы) по ID
      format-task    Изменить задачу(и)
      format-group   Переименовать группу

    ── add-task ─────────────────────────────────────────────
      python main_cli.py add-task [-t TITLE] [-s STATUS] [-g GROUP]
        -t, --title   Название задачи (default: "default task")
        -s, --status  Статус: active | frozen | finished
        -g, --group   Группа задачи (default: "default group")

    ── add-group ────────────────────────────────────────────
      python main_cli.py add-group [-t TITLE]
        -t, --title   Название группы (default: "default group")

    ── list-tasks ───────────────────────────────────────────
      python main_cli.py list-tasks [--sort SORT] [--filter] [--status STATUS] [--group GROUP]
        --sort   Сортировка: id | title | status | group_id
        --filter Включить фильтрацию
        --status Фильтр по статусу
        --group  Фильтр по группе

    ── list-groups ──────────────────────────────────────────
      python main_cli.py list-groups [--sort SORT]
        --sort   Сортировка: id | title

    ── delete-task ──────────────────────────────────────────
      python main_cli.py delete-task <id> [<id> ...]
        id      ID задачи(ей) для удаления

    ── delete-group ─────────────────────────────────────────
      python main_cli.py delete-group <id> [<id> ...]
        id      ID группы(групп) для удаления

    ── format-task ──────────────────────────────────────────
      python main_cli.py format-task <id> [<id> ...] [-t TITLE] [-s STATUS] [-g GROUP]
        id          ID задачи(ей) для изменения
        -t, --title  Новое название
        -s, --status Новый статус: active | frozen | finished
        -g, --group  Новая группа

    ── format-group ─────────────────────────────────────────
      python main_cli.py format-group <id> [-t TITLE]
        id          ID группы для переименования
        -t, --title  Новое название группы

    Защита default group:
      Группу "default group" нельзя удалить или переименовать.
      При удалении другой группы, её задачи переносятся в default group.
    """)

    def display_error(self, error: BaseException, command: str) -> None:
        traceback.print_exc()
        print(f"Unable to {command}, type '-h' for help\nERROR: {error}")
