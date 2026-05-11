import argparse

class CLIHandler:
    def __init__(self):
        # PARSER INIT
        self.parser = argparse.ArgumentParser(
            prog="main", description="Build your Task-List",
            add_help=True
        )
        self.subparsers = self.parser.add_subparsers(
            dest="command", required=True)
    
        self._init_add_task()
        self._init_add_group()
        self._init_list_tasks()
        self._init_list_groups()
        self._init_delete_task()
        self._init_delete_group()
        self._init_set_status()
        self._init_format_task()
        self._init_format_group()

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args

    def _init_add_task(self):
        parser_add_task = self.subparsers.add_parser("add-task", help="Add task")
        parser_add_task.add_argument("-t", "--title",   
                                        nargs='?', 
                                        help="Task`s title"
                                        )
        parser_add_task.add_argument("-s", "--status",
                                        choices=["active", "frozen", "finished"],
                                        nargs='?',
                                        default="active",
                                        help="Task status"
                                        )
        parser_add_task.add_argument("-g", "--group", 
                                        nargs='?', 
                                        default="ежедневные",
                                        help="Objects group"
                                        )
    
    def _init_add_group(self):
        parser_add_group = self.subparsers.add_parser("add-group", help="Add group")
        parser_add_group.add_argument("-t", "--title",
                                        nargs='?',
                                        help="Group`s title"
                                        )

    def _init_list_tasks(self):
        parser_list_tasks = self.subparsers.add_parser("list-tasks", help="Print all tasks")
        parser_list_tasks.add_argument("--sort", 
                                        choices=["title", "id", "status", "group", "priority",
                                                "deadline"],
                                        nargs='?',
                                        default="id",
                                        help="Type of tasks sorting"
                                        )
        parser_list_tasks.add_argument("--filter",
                                        action="store_true",
                                        help="Type of objects filter"
                                        )
        parser_list_tasks.add_argument("--status",
                                       nargs='?',
                                       help="Status for filter"
                                       )
        parser_list_tasks.add_argument("--group",
                                       nargs='?',
                                       help="Group for filter"
                                       )
    
    def _init_list_groups(self):
        parser_list_groups = self.subparsers.add_parser("list-groups", help="Print all groups")
        parser_list_groups.add_argument("--sort",
                                        choices=["title", "id"],
                                        nargs='?',
                                        default="id",
                                        help="Type of groups sorting"
                                        )
    
    def _init_delete_task(self):
        parser_delete_task = self.subparsers.add_parser("delete-task", help="Delete task")
        parser_delete_task.add_argument("id", 
                                        type=int,
                                        nargs='+', 
                                        help="Task`s ID"
                                        )
    
    def _init_delete_group(self):
        parser_delete_group = self.subparsers.add_parser("delete-group", help="Delete Group")
        parser_delete_group.add_argument("id", 
                                         type=int,
                                         nargs='+', 
                                         help="Group`s ID"
                                         )
    
    def _init_set_status(self):
        parser_set_status = self.subparsers.add_parser("set-status", help="Delete object")
        parser_set_status.add_argument("id",
                                        type=int,
                                        nargs='+', 
                                        help="Objects ID"
                                        )
        parser_set_status.add_argument("-s", "--status",
                                        choices=["active", "frozen", "finished"],
                                        help="Task status"
                                        )
    
    def _init_format_task(self):
        parser_format_task = self.subparsers.add_parser("format-task", help="Format task")
        parser_format_task.add_argument("id", 
                                        type=int,
                                        nargs='+', 
                                        help="Task`s ID"
                                        )
        parser_format_task.add_argument("-t", "--title", 
                                        nargs='?',
                                        help="Format task`s title"
                                        )
        parser_format_task.add_argument("-s", "--status",
                                        nargs='?',
                                        choices=["active", "frozen", "finished"],
                                        default="active",
                                        help="Format task`s title status"
                                        )
        parser_format_task.add_argument("-g", "--group", 
                                        nargs='?',
                                        default="ежедневные",
                                        help="Tasks group"
                                        )
    
    def _init_format_group(self):
        parser_format_group = self.subparsers.add_parser("format-group", help="Format group")
        parser_format_group.add_argument("id",
                                         type=int,
                                         nargs='+',
                                         help="Group`s ID"
                                         )
        parser_format_group.add_argument("-t", "--title",
                                         nargs='?',
                                         help="Format group`s title"
                                         )
