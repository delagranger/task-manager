import sys
import logging

from cli_argparser import CLIArgParser
from cli_output import CLIOutput
from task_manager import TaskManager

log = logging.getLogger(__name__)

class App:
    def __init__(self):
        try:
            self._argparser = CLIArgParser()
            self._output = CLIOutput()
            self._tm = TaskManager()
            log.debug("Init classes: SUCCESS")
        except Exception as e:
            log.critical("Init classes: FAILED\nERROR: %s", e)
            print("Critical ERROR\nERROR: %s", e)
            sys.exit(1)

    def run(self) -> None:
        try:
            args = self._argparser.parse_arguments()
            match args.command:
                case "add-task":
                    id, title, status, group = self._tm.add_task(args.title, args.status, args.group)
                    self._output.display_task_created(id, title, status, group)
                case "add-group":
                    id, title = self._tm.add_group(args.title)
                    self._output.display_group_created(id, title)
                case "list-tasks":
                    tasks = self._tm.list_tasks(args.sort, args.filter, args.status, args.group)
                    self._output.display_tasks(tasks)
                case "list-groups":
                    groups = self._tm.list_groups(args.sort)
                    self._output.display_groups(groups)
                case "delete-task":
                    ids = self._tm.delete_task(args.id)
                    self._output.display_tasks_deleted(ids)
                case "delete-group":
                    ids = self._tm.delete_group(args.id)
                    self._output.display_groups_deleted(ids)
                case "set-status":
                    ids, status = self._tm.set_status(args.id, args.status)
                    self._output.display_status_set(ids, status)
                case "format-task":
                    ids, title, status, group = self._tm.format_task(args.id, args.title, args.status, args.group)
                    self._output.display_task_formated(ids, title, status, group)
                case "format-group":
                    id, title = self._tm.format_group(args.id, args.title)
                    self._output.display_group_formated(id, title)
                case _:
                    self._output.display_incorrect_command(args.command)
        except Exception as e:
            try:
                self._output.display_error(e, args.command)
            except Exception as e:
                print("Unable to display error")
            

