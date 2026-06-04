class Task:
    def __init__(self, title, status, group):
        self.title = title
        self.status = status
        self.group = group


    def __str__(self):
        return "Type - Task; Title: %s; Status: %s; Group: %s" % (self.title, self.status, self.group)


    def __repr__(self):
        return "Type - Task; Title=%r; Status=%r; Group=%r" % (self.title, self.status, self.group)


