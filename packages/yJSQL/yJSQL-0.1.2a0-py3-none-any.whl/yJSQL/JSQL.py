import json
import copy

# Assuming custom exceptions are defined in the 'exceptions' module
from . import exceptions as JSQLE

class JSQL:

    def __init__(self, db_name: str) -> None:
        self.db_name: str = db_name
        self.__rollback_memory = None
        self.__transaction_stack = []  # Stack to support nested transactions
        self.__database: dict = self.__load_database(db_name)

    def __load_database(self, db_name: str) -> dict:
        try:
            with open(db_name, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            with open(db_name, 'w') as file:
                file.write("{}")
            return {}
        except json.JSONDecodeError:
            raise JSQLE.DataBaseWrongFormat(self.db_name)

    def create_table(self, table_name: str, columns: dict, primary_key: str = None, check_if_already_exists: bool = False) -> None:
        self.__rollback_memory = copy.deepcopy(self.__database)  # Store a deep copy

        if table_name in self.__database:
            if check_if_already_exists:
                return
            raise JSQLE.TableAlreadyExists(table_name, self.db_name)

        self.__database[table_name] = []  # Initialize empty table

        schema = {"columns": columns}
        if primary_key:
            schema["primary_key"] = primary_key

        self.__database[f"{table_name}_schema"] = schema
        self.__database[f"{table_name}_auto_increment"] = 1 if primary_key and columns.get(primary_key) == "int" else None


    def __validate_row(self, new_row: dict, table_name: str) -> bool:
        schema = self.__database.get(f"{table_name}_schema")
        if not schema:
            raise JSQLE.TableNotFound(table_name)

        columns = schema["columns"]
        unique_columns = schema.get("unique_columns", [])
        foreign_keys = schema.get("foreign_keys", {})

        for column_name, column_type in columns.items():
            if column_name not in new_row:
                raise JSQLE.MissingField(column_name, table_name)

            value = new_row[column_name]
            if not isinstance(value, eval(column_type)):
                raise JSQLE.WrongFieldType(column_name, column_type, type(value).__name__, table_name)

        for unique_column in unique_columns:
            if len([row for row in self.__database[table_name] if row.get(unique_column) == new_row.get(unique_column)]) > 0:
                raise JSQLE.UniqueConstraintViolation(unique_column, table_name)

        for fk_col, fk_table in foreign_keys.items():
            if not any(row.get(fk_col) == new_row.get(fk_col) for row in self.__database.get(fk_table, [])):
                raise JSQLE.ForeignKeyViolation(fk_col, fk_table, table_name)

        return True
    
    def count(self, table_name: str) -> int:

        if table_name not in self.__database:
            raise JSQLE.TableNotFound(table_name)
        
        return len(self.__database.keys())

    def insert(self, table_name: str, new_row: dict) -> None:
        self.__save_state()  # Save state before making changes

        if table_name not in self.__database:
            raise JSQLE.TableNotFound(table_name)

        self.__validate_row(new_row, table_name)
        self.__database[table_name].append(new_row)

    def select(self, table_name: str, where: dict = None, sort_by: str = None, ascending: bool = True, limit: int = None, offset: int = 0) -> list:
        if table_name not in self.__database:
            raise JSQLE.TableNotFound(table_name)

        table = self.__database.get(table_name, [])
        if where:
            table = [row for row in table if all(row.get(k) == v for k, v in where.items())]

        if sort_by:
            try:
                table = sorted(table, key=lambda x: x.get(sort_by), reverse=not ascending)
            except KeyError:
                raise JSQLE.ColumnNotFound(sort_by, table_name)

        if limit is not None:
            table = table[offset:offset + limit]

        return table

    def update(self, table_name: str, updates: dict, where: dict = None) -> None:
        self.__save_state()  # Save state before making changes

        if table_name not in self.__database:
            raise JSQLE.TableNotFound(table_name)

        table = self.__database.get(table_name, [])
        for row in table:
            if where is None or all(row.get(k) == v for k, v in where.items()):
                updated_row = {**row, **updates}
                self.__validate_row(updated_row, table_name)
                row.update(updates)

    def delete(self, table_name: str, where: dict = None) -> None:
        self.__save_state()  # Save state before making changes

        if table_name not in self.__database:
            raise JSQLE.TableNotFound(table_name)

        if where is None:
            # If no `where` condition is provided, delete all rows
            self.__database[table_name] = []
        else:
            # If a `where` condition is provided, delete matching rows
            table = self.__database.get(table_name, [])
            self.__database[table_name] = [
                row for row in table if not all(row.get(k) == v for k, v in where.items())
            ]

    def drop_table(self, table_name: str) -> None:
        self.__save_state()  # Save state before making changes

        if table_name not in self.__database:
            raise JSQLE.TableNotFound(table_name)

        self.__database.pop(table_name)
        self.__database.pop(f"{table_name}_schema", None)

    def commit(self) -> None:
        with open(self.db_name, 'w') as file:
            json.dump(self.__database, file, indent=4)
        self.__transaction_stack = []  # Clear the transaction stack after committing

    def rollback(self) -> None:
        if not self.__transaction_stack:
            raise JSQLE.RollbackError("No changes to rollback.")
        self.__database = self.__transaction_stack.pop()  # Restore the last state

    def begin_transaction(self) -> None:
        self.__transaction_stack.append(copy.deepcopy(self.__database))  # Save state

    def __save_state(self) -> None:
        if not self.__transaction_stack:  # Only save state if not already in a transaction
            self.__rollback_memory = copy.deepcopy(self.__database)
