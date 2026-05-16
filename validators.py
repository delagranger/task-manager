class Validator:
    def __init__(self, task_manager):
        self._tm = task_manager
    
    def is_group_id_exists(self, ids):
        for i in ids:
            flag = False
            for g in self._tm._groups:
                if g.id == i:
                    flag = True
                    break
            if not flag:
                raise GIDNotFound(i)
            
    def is_task_id_exists(self, ids):
        for i in ids:
            flag = False
            for t in self._tm._tasks:
                if t.id == i:
                    flag = True
                    break
            if not flag:
                raise TIDNotFound(i)
    
    def is_group_exists(self, group_title):
        flag = False
        for g in self._tm._groups:
            if g.title == group_title:
                flag = True
                break
        if not flag:
            raise GroupNotFound(group_title)

    def is_status_exists(self, status):
        flag = False
        for t in self._tm._tasks:
            if t.status == status:
                flag = True
                break
        if not flag:
            raise StatusNotFound(status)

    def is_group_not_exists(self, group_title):
        flag = True
        for g in self._tm._groups:
            if g.title == group_title:
                flag = False
                break
        if not flag:
            raise GroupAlreadyExists(group_title)

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
