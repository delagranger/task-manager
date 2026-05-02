class TaskManager:
    def __init__(self):
        pass
    # единоразово вызовет get_json_path
    # и сохранит его в атрибут экземпляра

    def get_json_path(self):
        pass
    # ищет файл .json по указанному пути
    # если нашли, то возвращаем путь к .json
    # если нет, то создаем .json и возвращаем путь к нему

    def save_data():
        pass
    # записываем обновленный список в .json

    def list_tasks(self):
        pass
    # выводит общий список задач

    def add_task(self):
        pass
    # из cli.parse_argument получаем название задачи
    # создаем экземпляр задачи
    # вызываем task.to_dict
    # записываем задачу в общий список задач
    # вызываем save_data