from operator import attrgetter

from task import Task
from group import Group
from file_manager import FileManager

class TaskManager:
    def __init__(self):
        self._file_manager = FileManager()
        self._next_task_id, self._next_group_id = self._file_manager.load_ids()
        self._tasks = self._file_manager.load_tasks()
        self._groups = self._file_manager.load_groups()

    def list_tasks(self, sort_type, status, group, filtered=False):
        filtered_tasks = self._tasks
        if filtered:
            if status:
                filtered_tasks = list(filter(lambda t: t.status == status, filtered_tasks))
            if group:
                filtered_tasks = list(filter(lambda t: t.group == group, filtered_tasks))

            print("filtered tasks -->")
            for i in filtered_tasks:
                print(f"""
                    ЗАДАЧА: {i.title}
                    ID: {i.id}
                    СТАТУС: {i.status}
                    ГРУППА: {i.group}
                    """)
            print("--------------")

        key = attrgetter(sort_type)
        sorted_tasks = sorted(filtered_tasks,
                    key=key, reverse=False
            )
        
        print("sorted tasks -->")
        for i in sorted_tasks:
            print(f"""
                    ЗАДАЧА: {i.title}
                    ID: {i.id}
                    СТАТУС: {i.status}
                    ГРУППА: {i.group}
                    """)
        print("--------------")
       
    def list_groups(self, sort_type):
        key = attrgetter(sort_type)
        sorted_groups = sorted(self._groups,
                    key=key, reverse=False
            )

        print("sorted groups -->")
        for i in sorted_groups:
            print(f"""
                    ГРУППА: {i.title}
                    ID: {i.id}
                    """)
        print("--------------")

    def add_task(self, title, status, group):
        task = Task(title, 
                    self._next_task_id,
                    status, group
                    )
        self._next_task_id += 1
        self._tasks.append(task) 

        self._file_manager.save_data(self._tasks, self._groups,
                                    self._next_task_id,
                                    self._next_group_id
                                    )

    def add_group(self, title):
        group = Group(title,
                    self._next_group_id
                    )
        self._next_group_id += 1
        self._groups.append(group)

        self._file_manager.save_data(self._tasks, self._groups,
                                    self._next_task_id,
                                    self._next_group_id
                                    )

    def delete_task(self, id):
        for i in id:
            for j in self._tasks:
                if j.id == i:
                    self._tasks.remove(j)
                    break

        self._file_manager.save_data(self._tasks, self._groups,
                                    self._next_task_id,
                                    self._next_group_id
                                    )

    def delete_group(self, id):
        for i in id:
            for j in self._groups:
                if j.id == i:
                    self._groups.remove(j)
                    break

        self._file_manager.save_data(self._tasks, self._groups,
                                    self._next_task_id,
                                    self._next_group_id
                                    )

    def set_status(self, id, status):
        for i in id:
            for j in self._tasks:
                if j.id == i:
                    j.status = status
                    break
        
        self._file_manager.save_data(self._tasks, self._groups,
                                    self._next_task_id,
                                    self._next_group_id
                                    )

    def format_task(self, id, title, status, group):
        for i in id:
            for j in self._tasks:
                if j.id == i:
                    j.title = title
                    j.status = status
                    j.group = group
                    break
        
        self._file_manager.save_data(self._tasks, self._groups,
                                    self._next_task_id,
                                    self._next_group_id
                                    )

    def format_group(self, id, title):
        for i in id:
            for j in self._groups:
                if j.id == i:
                    j.title = title
        
        self._file_manager.save_data(self._tasks, self._groups,
                                    self._next_task_id,
                                    self._next_group_id
                                    )

