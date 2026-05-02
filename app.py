class App:
    def __init__(self):
        pass

    def run(self, args):
        pass
    # получаем args из main, args - список
    # передаем args в cli.parse_arguments
    # получаем args_dict из cli.parse_arguments
    # сравниваем элемент "command" из словаря через условный оператор
    # в зависимости от команды вызываем различные функции класса TaskManager