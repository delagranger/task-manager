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
        parser_add.add_argument("title", help="Title of the object")
        parser_add.add_argument("status",
                                choices=["active", "frozen", "finished"],
                                default="active",
                                help="Task status")

        # LIST
        parser_list = self.subparsers.add_parser("list", help="Print all objects")
        parser_list.add_argument("sort_type", 
                                 choices=["title", "id", "status"],
                                 help="Type of objects sorting")

        # DELETE
        parser_delete = self.subparsers.add_parser("delete", help="Delete object")
        parser_delete.add_argument("obj_link", nargs="+", help="Link to object (title, id)")

        # SET_STATUS
        parser_setstatus = self.subparsers.add_parser("set_status", help="Delete object")
        parser_setstatus.add_argument("obj_link", nargs="+", help="Link to object (title, id)")
        parser_setstatus.add_argument("status",
                                choices=["active", "frozen", "finished"],
                                help="Task status")

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args