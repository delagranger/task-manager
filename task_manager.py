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
            print(f"ЗАДАЧА: {i.title} | ID: {i.id} | STATUS: {i.status}")

    def add(self, title, status):
        task = Task(title, 
                    self.file_manager.next_task_id,
                    status)
        self.file_manager.next_task_id += 1
        self.file_manager.tasks.append(task)
        self.file_manager.save_data()
    
    def delete(self, id):
        for i in id:
            for j in self.file_manager.tasks:
                if str(j.id) == i:
                    self.file_manager.tasks.remove(j)
                    break

        self.file_manager.save_data()
    
    def set_status(self, id, status):
        for i in id:
            for j in self.file_manager.tasks:
                if str(j.id) == i:
                    j.status = status
                    break
        
        self.file_manager.save_data()
    
    def format(self, id, title, status):
        for i in id:
            for j in self.file_manager.tasks:
                if str(j.id) == i:
                    j.title = title
                    j.status = status
                    break
        
        self.file_manager.save_data()
