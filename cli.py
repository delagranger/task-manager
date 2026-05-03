class CLIHandler:
    def __init__(self):
        pass

    def show_commands(self):
        pass
    
    def parse_arguments(self, args):
        args_dict = {}

        if args[0] == "add":
            args_dict["command"] = "add"
            if len(args) > 1:
                args_dict["title"] = args[1]
        elif args[0] == "list":
            args_dict["command"] = "list"
        
        return args_dict