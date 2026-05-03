from cli import CLIHandler
from manager import TaskManager

class App:
    def __init__(self):
        self.cli = CLIHandler()
        self.manager = TaskManager()

    def run(self):
        args = self.cli.parse_arguments()

        if args.command == "add":
            self.manager.add_task(args.title)
        elif args.command == "list":
            self.manager.list_tasks()
