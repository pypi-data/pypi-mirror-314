# JSQL - JSON SQL-like Database

`JSQL` is a lightweight SQL-like database system that stores data in a JSON file. It supports common database operations such as creating tables, inserting data, updating data, and querying data. Transactions and rollback functionality are also supported.

## Features

- **Table Creation:** Create tables with specified columns and optional primary keys.
- **Data Insertion:** Insert rows into tables with automatic type validation.
- **Data Selection:** Query data with filtering, sorting, and pagination.
- **Data Updating:** Update rows in tables with automatic type validation.
- **Data Deletion:** Delete rows from tables with filtering.
- **Transactions:** Support for nested transactions, rollback, and commit operations.
- **Constraints:** Supports unique constraints, foreign key constraints, and field type validation.

## Installation

To install `JSQL`, simply clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/JSQL.git
```

## Usage

### Initialization

To use `JSQL`, initialize a `JSQL` object with the name of the database (a JSON file):

```python
from JSQL import JSQL

db = JSQL("my_database.json")
```

This will load the database from `my_database.json` or create a new empty database if the file does not exist.

### Table Creation

You can create tables by specifying the table name, columns, and an optional primary key:

```python
columns = {
    "id": "int",
    "name": "str",
    "age": "int",
}

db.create_table("users", columns, primary_key="id")
```

If the table already exists, you can choose to ignore the creation by setting the `check_if_already_exists` flag to `True`:

```python
db.create_table("users", columns, primary_key="id", check_if_already_exists=True)
```

### Inserting Data

Insert a row into a table:

```python
new_user = {
    "id": 1,
    "name": "Alice",
    "age": 30
}

db.insert("users", new_user)
```

### Querying Data

Select data from a table with optional filtering, sorting, and pagination:

```python
# Select all users
users = db.select("users")

# Select users with a filter
young_users = db.select("users", where={"age": 30})

# Select users sorted by age, in descending order
sorted_users = db.select("users", sort_by="age", ascending=False)

# Select users with pagination (limit and offset)
paginated_users = db.select("users", limit=10, offset=20)
```

### Updating Data

Update rows in a table:

```python
# Update the age of users named "Alice"
db.update("users", updates={"age": 31}, where={"name": "Alice"})
```

### Deleting Data

Delete rows from a table:

```python
# Delete users aged 31
db.delete("users", where={"age": 31})

# Delete all rows in the table
db.delete("users")
```

### Transactions

Begin a transaction, make changes, and either commit or rollback:

```python
db.begin_transaction()

# Make some changes
db.insert("users", {"id": 2, "name": "Bob", "age": 25})

# Commit the changes
db.commit()

# If something goes wrong, you can rollback instead of committing
db.rollback()
```

### Handling Errors

`JSQL` includes custom exceptions for error handling:

```python
from JSQL.exceptions import TableNotFound, MissingField

try:
    db.insert("nonexistent_table", {"id": 1})
except TableNotFound as e:
    print(e)
```

Some available exceptions:

- `DataBaseWrongFormat`: Raised when the database file is corrupted.
- `TableAlreadyExists`: Raised when trying to create a table that already exists.
- `MissingField`: Raised when inserting/updating a row with missing fields.
- `WrongFieldType`: Raised when a field has an incorrect data type.
- `TableNotFound`: Raised when the specified table is not found.
- `RollbackError`: Raised when there's nothing to rollback.

## Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
