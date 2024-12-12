class DataBaseWrongFormat(Exception):
    def __init__(self, db_name: str) -> None:
        super().__init__(f"{db_name} format is corrupted, delete it or try fixing it manually")

class TableAlreadyExists(Exception):
    def __init__(self, table_name: str, db_name: str) -> None:
        super().__init__(f"The table '{table_name}' already exists in '{db_name}'")

class MissingField(Exception):
    def __init__(self, field_name: str, table_name: str) -> None:
        super().__init__(f"Missing value for field '{field_name}' in table '{table_name}'")

class WrongFieldType(Exception):
    def __init__(self, field_name: str, expected_type: str, actual_type: str, table_name: str) -> None:
        super().__init__(f"Field '{field_name}' in table '{table_name}' should be of type '{expected_type}', but got '{actual_type}'")

class TableNotFound(Exception):
    def __init__(self, table_name: str) -> None:
        super().__init__(f"The table '{table_name}' was not found")

class RollbackError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class InvalidColumnType(Exception):
    def __init__(self, column_name: str, expected_type: str) -> None:
        super().__init__(f"Invalid type for column '{column_name}'. Expected '{expected_type}'")

class ConstraintViolation(Exception):
    def __init__(self, constraint: str, table_name: str) -> None:
        super().__init__(f"Constraint '{constraint}' violated in table '{table_name}'")

class ColumnAlreadyExists(Exception):
    def __init__(self, column_name: str, table_name: str) -> None:
        super().__init__(f"Column '{column_name}' already exists in table '{table_name}'")
