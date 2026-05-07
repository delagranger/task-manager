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
        if args.command == "add":
            self.manager.add(args.obj_type, args.title, args.status, args.group)
        elif args.command == "list":
            self.manager.list(args.obj_type, args.sort_type)
        elif args.command == "delete":
            self.manager.delete(args.id)
        elif args.command == "set_status":
            self.manager.set_status(args.id, args.status)
        elif args.command == "format":
            self.manager.format(args.id, args.title, args.status, args.group)
