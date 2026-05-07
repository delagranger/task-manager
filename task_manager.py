from operator import attrgetter

from objects import Task
from file_manager import FileManager

class TaskManager:
    def __init__(self):
        self.file_manager = FileManager()

    def list(self, sort_type):
        key = attrgetter(sort_type)
        self.file_manager.tasks.sort(
            key=key, reverse=False
        )

        for i in self.file_manager.tasks:
            print(f"ЗАДАЧА: {i.title} | ID: {i.id}")

    def add(self, title):
        task = Task(title, self.file_manager.next_task_id)
        self.file_manager.next_task_id += 1
        self.file_manager.tasks.append(task)
        self.file_manager.save_data()
    
    def delete(self, obj_link):
        for i in obj_link:
            for j in self.file_manager.tasks:
                if int(j.id) == i or j.title == i:
                    self.file_manager.tasks.remove(j)
                    break

        self.file_manager.save_data()
