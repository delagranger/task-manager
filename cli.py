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

#--------------------------------------------------------------------------------------------------

        # ADD-TASK
        parser_add_task = self.subparsers.add_parser("add-task", help="Add task")
        parser_add_task.add_argument("-t", "--title",   
                                nargs='?', 
                                help="Task`s title")
        parser_add_task.add_argument("-s", "--status",
                                choices=["active", "frozen", "finished"],
                                nargs='?',
                                default="active",
                                help="Task status")
        parser_add_task.add_argument("-g", "--group", 
                                nargs='?', 
                                default="ежедневные",
                                help="Objects group")
        
        # ADD-GROUP
        parser_add_group = self.subparsers.add_parser("add-group", help="Add group")
        parser_add_group.add_argument("-t", "--title",
                                      nargs='?',
                                      help="Group`s title"
                                      )

#--------------------------------------------------------------------------------------------------

        # LIST-TASKS
        parser_list_tasks = self.subparsers.add_parser("list-tasks", help="Print all tasks")
        parser_list_tasks.add_argument("-s", "--sort", 
                                choices=["title", "id", "status", "group", "priority",
                                         "deadline"],
                                nargs='?',
                                default="id",
                                help="Type of tasks sorting")
        # parser_list.add_argument("-f", "--filter",
        #                          choices=["status", "group", "priority", "deadline"],
        #                          nargs='?',
        #                          help="Type of objects filter"
        #                          )

        # LIST-GROUPS
        parser_list_groups = self.subparsers.add_parser("list-groups", help="Print all groups")
        parser_list_groups.add_argument("-s", "--sort",
                                        choices=["title", "id"],
                                        nargs='?',
                                        default="id",
                                        help="Type of groups sorting"
                                        )

#--------------------------------------------------------------------------------------------------

        # DELETE-TASK
        parser_delete_task = self.subparsers.add_parser("delete-task", help="Delete task")
        parser_delete_task.add_argument("id", 
                                        type=int,
                                        nargs='+', 
                                        help="Task`s ID")

        # DELETE-GROUP
        parser_delete_group = self.subparsers.add_parser("delete-group", help="Delete Group")
        parser_delete_group.add_argument("id", 
                                         type=int,
                                         nargs='+', 
                                         help="Group`s ID")

#--------------------------------------------------------------------------------------------------

        # SET_STATUS
        parser_set_status = self.subparsers.add_parser("set-status", help="Delete object")
        parser_set_status.add_argument("id",
                                      type=int,
                                      nargs='+', 
                                      help="Objects ID")
        parser_set_status.add_argument("-s", "--status",
                                choices=["active", "frozen", "finished"],
                                help="Task status")

#--------------------------------------------------------------------------------------------------
    
        # FORMAT-TASK
        parser_format_task = self.subparsers.add_parser("format-task", help="Format task")
        parser_format_task.add_argument("id", 
                                   type=int,
                                   nargs='+', 
                                   help="Task`s ID")
        parser_format_task.add_argument("-t", "--title", 
                                   nargs='?',
                                   help="Format task`s title")
        parser_format_task.add_argument("-s", "--status",
                                   nargs='?',
                                   choices=["active", "frozen", "finished"],
                                   default="active",
                                   help="Format task`s title status")
        parser_format_task.add_argument("-g", "--group", 
                                   nargs='?',
                                   default="ежедневные",
                                   help="Tasks group")
        
        # FORMAT-GROUP
        parser_format_group = self.subparsers.add_parser("format-group", help="Format group")
        parser_format_group.add_argument("id",
                                         type=int,
                                         nargs='+',
                                         help="Group`s ID")
        parser_format_group.add_argument("-t", "--title",
                                         nargs='?',
                                         help="Format group`s title")

#--------------------------------------------------------------------------------------------------

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args