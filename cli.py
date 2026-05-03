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

        # LIST
        parser_list = self.subparsers.add_parser("list", help="Print all objects")

        # DELETE
        parser_delete = self.subparsers.add_parser("delete", help="Delete object")
        parser_delete.add_argument("title", help="Title of the object")

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args