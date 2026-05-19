from exceptions import *

class Validator:
    def __init__(self, task_manager):
        self._tm = task_manager
    
    def verify_group_id_exists(self, ids):
        for i in ids:
            exists = False
            for g in self._tm._groups:
                if g.id == i:
                    exists = True
                    break
            if not exists:
                raise GIDNotFound(i)
            
    def verify_task_id_exists(self, ids):
        for i in ids:
            exists = False
            for t in self._tm._tasks:
                if t.id == i:
                    exists = True
                    break
            if not exists:
                raise TIDNotFound(i)
    
    def verify_group_exists(self, group_title, expected_exist = True):
        exists = False
        for g in self._tm._groups:
            if g.title == group_title:
                exists = True
                break
        if not exists and expected_exist:
            raise GroupNotFound(group_title)
        elif exists and not expected_exist:
            raise GroupAlreadyExists(group_title)

    def verify_status_exists(self, status):
        exists = False
        for t in self._tm._tasks:
            if t.status == status:
                exists = True
                break
        if not exists:
            raise StatusNotFound(status)

