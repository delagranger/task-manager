import sys
import logging

from .cli_argparser import CLIArgParser
from .cli_output import CLIOutput
from services import TaskManager
from auth import AuthManager

log = logging.getLogger(__name__)

class App:
    def __init__(self):
        try:
            self._argparser = CLIArgParser()
            self._output = CLIOutput()
            self._tm = TaskManager()
            self._auth = AuthManager()
            log.debug("Init classes: SUCCESS")
        except Exception as e:
            log.critical("Init classes: FAILED\nERROR: %s", e)
            print("Critical ERROR\nERROR: %s", e)
            sys.exit(1)


    def run(self) -> None:
        args = None
        try:
            args = self._argparser.parse_arguments()
            if args.help or not args.command:
                self._output.display_help()
                return
            match args.command:
                case "add-task":
                    id, title, status, group = self._tm.add_task(
                        args.title, args.status, args.group,
                    )
                    self._output.display_task_created(
                        id, title, status, group,
                    )
                case "add-group":
                    id, title = self._tm.add_group(args.title)
                    self._output.display_group_created(id, title)
                case "list-tasks":
                    tasks = self._tm.list_tasks(
                        args.sort, args.filter, args.status, args.group,
                    )
                    self._output.display_tasks(tasks)
                case "list-groups":
                    groups = self._tm.list_groups(args.sort)
                    self._output.display_groups(groups)
                case "delete-task":
                    for task_id in args.id:
                        deleted_id = self._tm.delete_task(task_id)
                        self._output.display_tasks_deleted(deleted_id)
                case "delete-group":
                    for group_id in args.id:
                        deleted_id = self._tm.delete_group(group_id)
                        self._output.display_groups_deleted(deleted_id)
                case "format-task":
                    ids, title, status, group = self._tm.format_task(
                        args.id, args.title, args.status, args.group,
                    )
                    self._output.display_task_formated(
                        ids, title, status, group,
                    )
                case "format-group":
                    id, title = self._tm.format_group(args.id, args.title)
                    self._output.display_group_formated(id, title)
                case "register":
                    id, login = self._auth.register(args.login, args.passwords)
                    self._output.display_registration_complete(id, login)
                case "login":
                    id, login = self._auth.login(args.login, args.password)
                    self._output.display_login_complete(id, login)
                case _:
                    self._output.display_incorrect_command(args.command)
        except Exception as e:
            command = args.command if args else "unknown"
            self._output.display_error(e, command)
            