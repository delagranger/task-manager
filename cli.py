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

        # ADD
        parser_add = self.subparsers.add_parser("add", help="Add task or group")
        parser_add.add_argument("obj_type", 
                                choices=["task", "group"], 
                                help="Type of object (group or task)")
        parser_add.add_argument("title", 
                                help="Title of the object")
        parser_add.add_argument("status",
                                choices=["active", "frozen", "finished"],
                                nargs='?',
                                default="active",
                                help="Task status")
        parser_add.add_argument("group", 
                                nargs='?', 
                                default="ежедневные",
                                help="Objects group")

        # LIST
        parser_list = self.subparsers.add_parser("list", help="Print all objects")
        parser_list.add_argument("obj_type", 
                                choices=["task", "group"], 
                                help="Type of object (group or task)")
        parser_list.add_argument("sort_type", 
                                choices=["title", "id", "status", "group"],
                                nargs='?',
                                default="id",
                                help="Type of objects sorting")

        # DELETE
        parser_delete = self.subparsers.add_parser("delete", help="Delete object")
        parser_delete.add_argument("id", nargs='+', help="Objects ID")

        # SET_STATUS
        parser_setstatus = self.subparsers.add_parser("set_status", help="Delete object")
        parser_setstatus.add_argument("id", 
                                      nargs='+', 
                                      help="Objects ID")
        parser_setstatus.add_argument("status",
                                choices=["active", "frozen", "finished"],
                                help="Task status")
    
        # FORMAT
        parser_format = self.subparsers.add_parser("format", help="Format object")
        parser_format.add_argument("id", nargs='+', 
                                   help="Objects ID")
        parser_format.add_argument("title", 
                                   help="Format object`s title")
        parser_format.add_argument("status",
                                   nargs='?',
                                   choices=["active", "frozen", "finished"],
                                   default="active",
                                   help="Format object`s title status")
        parser_format.add_argument("group", 
                                   nargs='?',
                                   default="ежедневные",
                                   help="Tasks group")

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args