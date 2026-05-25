class Task:
    def __init__(self, title, status, group):
        self.title = title
        self.status = status
        self.group = group
    
    @classmethod
    def print_task(self, task):
        print(f"""
                ЗАДАЧА: {task[1]}
                ID: {task[0]}
                СТАТУС: {task[2]}
                ГРУППА: {task[3]}
        """)


