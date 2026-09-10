class ValidationError(Exception):
    pass


class StatusNotFound(ValidationError):
    def __init__(self, status: str, statuses: list[str]) -> None:
        super().__init__(f"Status '{status}' is not found. Possible statuses: {statuses}")


class GIDNotFound(ValidationError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Group with ID {id} is not found")


class TIDNotFound(ValidationError):
    def __init__(self, ids: list[int]) -> None:
        super().__init__(f"Task with ID {ids} is not found")


class GroupNotFound(ValidationError):
    def __init__(self, title: str) -> None:
        super().__init__(f"Group '{title}' is not found")


class GroupAlreadyExists(ValidationError):
    def __init__(self, title: str) -> None:
        super().__init__(f"Group {title} is already exists")


class SortTypeNotFound(ValidationError):
    def __init__(self, sort_type: str, sort_types: list[str]) -> None:
        super().__init__(f"Sort type '{sort_type}' is not found. Possible sort types: {sort_types}")


class FilterNotExists(ValidationError):
    def __init__(self) -> None:
        super().__init__(f"No filter specified")


class IncorrectLength(ValidationError):
    def __init__(self, obj_type: str, cur_length: int, max_length: int) -> None:
        super().__init__(
            f"{str(obj_type).capitalize()} length is too large. "
            f"Current length is {cur_length}. Max length for {obj_type} is {max_length}"
        )


class DefaultGroupProtectedError(ValidationError):
    def __init__(self, action: str) -> None:
        super().__init__(f"Cannot {action} the default group. The default group is protected.")


class DifferentPasswords(ValidationError):
    def __init__(self) -> None:
        super().__init__(f"Passwords are different! Rewrite the passwords so that they are identical")
