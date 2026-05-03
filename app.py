from cli import CLIHandler
from task_manager import TaskManager

class App:
    def __init__(self):
        self.cli = CLIHandler()
        self.manager = TaskManager()

    def run(self):
        args = self.cli.parse_arguments()

        if args.command == "add":
            self.manager.add(args.title)
        elif args.command == "list":
            self.manager.list()
        elif args.command == "delete":
            self.manager.delete(args.title)
