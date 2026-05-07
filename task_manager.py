from operator import attrgetter

from objects import Task
from objects import Group
from file_manager import FileManager

class TaskManager:
    def __init__(self):
        self.file_manager = FileManager()

    def list_tasks(self, sort_type):
        key = attrgetter(sort_type)
        sorted_tasks = sorted(self.file_manager.tasks,
                    key=key, reverse=False
            )

        for i in sorted_tasks:
            print(f"""
ЗАДАЧА: {i.title}
ID: {i.id}
СТАТУС: {i.status}
ГРУППА: {i.group}
                    """)
            
    def list_groups(self, sort_type):
        key = attrgetter(sort_type)
        sorted_groups = sorted(self.file_manager.groups,
                    key=key, reverse=False
            )

        for i in sorted_groups:
            print(f"""
ГРУППА: {i.title}
ID: {i.id}
                    """)

    def add_task(self, title, status, group):
        task = Task(title, 
                    self.file_manager.next_task_id,
                    status, group)
        self.file_manager.next_task_id += 1
        self.file_manager.tasks.append(task) 

        self.file_manager.save_data()
    
    def add_group(self, title):
        group = Group(title,
                    self.file_manager.next_group_id)
        self.file_manager.next_group_id += 1
        self.file_manager.groups.append(group)

        self.file_manager.save_data()
    
    def delete_task(self, id):
        for i in id:
            for j in self.file_manager.tasks:
                if j.id == i:
                    self.file_manager.tasks.remove(j)
                    break

        self.file_manager.save_data()
    
    def delete_group(self, id):
        for i in id:
            for j in self.file_manager.groups:
                if j.id == i:
                    self.file_manager.groups.remove(j)
                    break

        self.file_manager.save_data()
    
    def set_status(self, id, status):
        for i in id:
            for j in self.file_manager.tasks:
                if j.id == i:
                    j.status = status
                    break
        
        self.file_manager.save_data()
    
    def format_task(self, id, title, status, group):
        for i in id:
            for j in self.file_manager.tasks:
                if j.id == i:
                    j.title = title
                    j.status = status
                    j.group = group
                    break
        
        self.file_manager.save_data()
    
    def format_group(self, id, title):
        for i in id:
            for j in self.file_manager.groups:
                if j.id == i:
                    j.title = title
        
        self.file_manager.save_data()
