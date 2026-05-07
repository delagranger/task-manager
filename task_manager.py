from operator import attrgetter

from objects import Task
from objects import Group
from file_manager import FileManager

class TaskManager:
    def __init__(self):
        self.file_manager = FileManager()

    def list(self, obj_type, sort_type):
        key = attrgetter(sort_type)

        if obj_type == "task":
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
        elif obj_type == "group":
            sorted_groups = sorted(self.file_manager.groups,
                key=key, reverse=False
            )

            for i in sorted_groups:
                print(f"""
                    ГРУППА: {i.title}
                    ID: {i.id}
                    """)

    def add(self, obj_type, title, status, group):
        if obj_type == "task":
            task = Task(title, 
                        self.file_manager.next_task_id,
                        status, group)
            self.file_manager.next_task_id += 1
            self.file_manager.tasks.append(task) 
        elif obj_type == "group":
            group = Group(title,
                          self.file_manager.next_group_id)
            self.file_manager.next_group_id = 'g' + str(
                int(self.file_manager.next_group_id[1:]) + 1
            )
            self.file_manager.groups.append(group)

        self.file_manager.save_data()
    
    def delete(self, id):
        for i in id:
            if i[0] == 'g':
                for j in self.file_manager.groups:
                    if j.id == i:
                        self.file_manager.groups.remove(j)
                        break
            else:
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
    
    def format(self, id, title, status, group):
        for i in id:
            if i[0] == 'g':
                for j in self.file_manager.groups:
                    if j.id == i:
                        j.title = title
                        break
            else:
                for j in self.file_manager.tasks:
                    if str(j.id) == i:
                        j.title = title
                        j.status = status
                        j.group = group
                        break
        
        self.file_manager.save_data()
