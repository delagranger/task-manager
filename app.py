from cli import CLIHandler
from manager import TaskManager

class App:
    def __init__(self):
        self.cli = CLIHandler()
        self.manager = TaskManager()

    def run(self, args):
        args_dict = self.cli.parse_arguments(args)

        if args_dict["command"] == "add":
            self.manager.add_task(args_dict["title"])
        elif args_dict["command"] == "list":
            self.manager.list_tasks()