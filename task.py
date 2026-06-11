class Task:
    def __init__(self, title, status, group):
        self.title = title
        self.status = status
        self.group = group


    def __repr__(self):
        return f"Task(Title={self.title}, status={self.status}, group={self.group})"


