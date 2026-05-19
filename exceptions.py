class ValidationError(Exception):
        pass

class GIDNotFound(ValidationError):
    def __init__(self, group_id):
        self.group_id = group_id
        super().__init__(f"Group with ID {group_id} is not found")

class TIDNotFound(ValidationError):
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} is not found")

class GroupNotFound(ValidationError):
    def __init__(self, group):
        self.group = group
        super().__init__(f"Group '{group}' is not found")

class StatusNotFound(ValidationError):
    def __init__(self, status):
        self.status = status
        super().__init__(f"Status '{status}' is not found")

class GroupAlreadyExists(ValidationError):
    def __init__(self, group):
        self.group = group
        super().__init__(f"Group '{group}' already exists")