from cli import CLIHandler
from task_manager import TaskManager

class App:
    def __init__(self):
        self.cli = CLIHandler()
        self.manager = TaskManager()

    def run(self):
        args = self.cli.parse_arguments()
        # получение команды и параметров из консоли 
        # в виде пространства имен
        # прим. args = Namespace(command='delete', obj_link=['1', '2'])

        # вызов различных функций manager
        match args.command:
            case "add-task":
                self.manager.add_task(args.title, args.status, 
                                      args.group
                                      )
            case "add-group":
                self.manager.add_group(args.title)
            case "list-tasks":
                self.manager.list_tasks(args.sort, args.status, 
                                        args.group, args.filter
                                        )
            case "list-groups":
                self.manager.list_groups(args.sort)
            case "delete-task":
                self.manager.delete_task(args.id)
            case "delete-group":
                self.manager.delete_group(args.id)
            case "set-status":
                self.manager.set_status(args.id, args.status)
            case "format-task":
                self.manager.format_task(args.id, args.title, 
                                         args.status, args.group
                                         )
            case "format-group":
                self.manager.format_group(args.id, args.title)
            case _:
                print("Unknown command")
            

