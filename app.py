import logging

from cli import CLIHandler
from task_manager import TaskManager

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)
logger.info(f"Logging is started, level {logging.getLevelName(logging.getLogger().getEffectiveLevel())}")

class App:
    def __init__(self):
        self._cli = CLIHandler()
        self._manager = TaskManager()

    def run(self):
        args = self._cli.parse_arguments()
        # получение команды и параметров из консоли 
        # в виде пространства имен
        # прим. args = Namespace(command='delete', obj_link=['1', '2'])

        # вызов различных функций manager
        match args.command:
            case "add-task":
                self._manager.add_task(args.title, args.status, 
                                      args.group
                                      )
            case "add-group":
                self._manager.add_group(args.title)
            case "list-tasks":
                self._manager.list_tasks(args.sort, args.status, 
                                        args.group, args.filter
                                        )
            case "list-groups":
                self._manager.list_groups(args.sort)
            case "delete-task":
                self._manager.delete_task(args.id)
            case "delete-group":
                self._manager.delete_group(args.id)
            case "set-status":
                self._manager.set_status(args.id, args.status)
            case "format-task":
                self._manager.format_task(args.id, args.title, 
                                         args.status, args.group
                                         )
            case "format-group":
                self._manager.format_group(args.id, args.title)
            case _:
                print("Unknown command")
            

