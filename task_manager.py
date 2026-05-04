from objects import Task
from file_manager import FileManager

class TaskManager:
    def __init__(self):
        self.file_manager = FileManager()

    def list(self):
        for i in self.file_manager.tasks:
            print(i)

    def add(self, title):
        task = Task(title)
        self.file_manager.tasks.append(task)
        self.file_manager.save_data()
    
    def delete(self, title):
        for i in self.file_manager.tasks:
            if i.title == title:
                self.file_manager.tasks.remove(i)
                break

        self.file_manager.save_data()
