class ValidationError(Exception):
        pass


class GIDNotFound(ValidationError):
    def __init__(self, id):
        self.group_id = id
        super().__init__(f"Group with ID {id} is not found")


class TIDNotFound(ValidationError):
    def __init__(self, ids):
        self.task_id = ids
        super().__init__(f"Task with ID {ids} is not found")


class GroupNotFound(ValidationError):
    def __init__(self, title):
        self.group = title
        super().__init__(f"Group '{title}' is not found")


class StatusNotFound(ValidationError):
    def __init__(self, status):
        self.status = status
        super().__init__(f"Status '{status}' is not found")


class SortTypeNotFound(ValidationError):
    def __init__(self, sort_type):
        self.sort_type = sort_type
        super().__init__(f"Sort type '{sort_type}' is not found")


class FilterNotExists(ValidationError):
    def __init__(self):
        super().__init__(f"No filter specified")
