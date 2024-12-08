import sqlite3

# Usage example
TABLE_NAME = "clutchgames"
EXPECTED_COLUMNS = [
    ("id", "INTEGER PRIMARY KEY"),
    ("gameid", "TEXT NOT NULL"),
    ("alert_time", "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"),
    ("alert_sent", "BOOLEAN NOT NULL DEFAULT 0"),
    ("overtime_alert_number", "INTEGER NOT NULL DEFAULT 0"),
]


def check_and_recreate_table(
    db_name: str, table_name: str, expected_columns: list[tuple[str, str]]
) -> True:
    """
    Checks if a table exists in a SQLite database and recreates it if the schema does not match the expected columns.

    Args:
        db_name (str): The name of the SQLite database file.
        table_name (str): The name of the table to check or recreate.
        expected_columns (list[tuple]): A list of tuples, where each tuple is (column_name, column_type).

    Returns:
        None
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Check if table exists
    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    )
    table_exists = cursor.fetchone() is not None
    if table_exists:
        # Get the current schema of the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        current_schema = [(row[1], row[2]) for row in cursor.fetchall()]

        # Check if the schema matches the expected schema
        if current_schema != expected_columns:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        else:
            connection.close()
            return

    # Recreate the table with the correct schema
    columns_definition = ", ".join(f"{col} {dtype}" for col, dtype in expected_columns)
    cursor.execute(f"CREATE TABLE {table_name} ({columns_definition});")

    # Commit changes and close the connection
    connection.commit()
    connection.close()


def clear_table(db_name: str, table_name: str):
    """
    Clear all rows from the given table in the given database.

    Args:
        db_name (str): The name of the SQLite database file.
        table_name (str): The name of the table to clear.

    Returns:
        None
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_name};")
    connection.commit()
    connection.close()


def insert_game(db_name: str, table_name: str, gameid: str):
    """
    Insert a new row into the given table in the given database.

    The new row will have the given gameid and the alert_sent column will be set to 0.

    Args:
        db_name (str): The name of the SQLite database file.
        table_name (str): The name of the table to insert into.
        gameid (str): The gameid to insert.

    Returns:
        None
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {table_name} (gameid) VALUES ('{gameid}');")
    connection.commit()
    connection.close()


def update_alert_sent(db_name: str, table_name: str, gameid: str):
    """
    Update the alert_sent column to 1 for the given
    gameid in the given table and database.

    Args:
        db_name (str): The name of the SQLite database file.
        table_name (str): The name of the table to update.
        gameid (str): The gameid to update.

    Returns:
        None
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"UPDATE {table_name} SET alert_sent = 1 WHERE gameid = '{gameid}';")
    connection.commit()
    connection.close()


def check_alert_sent(db_name: str, table_name: str, gameid: str):
    """
    Check if the alert has been sent for the given gameid in the specified table and database.

    Args:
        db_name (str): The name of the SQLite database file.
        table_name (str): The name of the table to check.
        gameid (str): The gameid to check.

    Returns:
        bool: True if the alert has been sent (alert_sent is not None), otherwise False.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT alert_sent FROM {table_name} WHERE gameid = '{gameid}';")
    results = cursor.fetchone()
    alert_sent = results is not None and results[0]
    connection.close()
    return alert_sent


def check_overtime_alert_sent(
    db_name: str, table_name: str, gameid: str, overtime_number: int
):
    """
    Check if the alert has been sent for the given gameid in the specified table and database.

    Args:
        db_name (str): The name of the SQLite database file.
        table_name (str): The name of the table to check.
        gameid (str): The gameid to check.
        overtime_number (int): The overtime number to check

    Returns:
        bool: True if the alert has been sent (alert_sent is not None), otherwise False.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"""
                   SELECT overtime_alert_number FROM {table_name} 
                   WHERE gameid = '{gameid}' AND 
                   overtime_alert_number = {overtime_number};
                   """)
    alert_sent = cursor.fetchone() is not None
    connection.close()
    return alert_sent


def update_overtime_number(db_name: str, table_name: str, gameid: str):
    """
    Increament the overtime alert number for the given gameid in the specified table and database.

    Args:
        db_name (str): The name of the SQLite database file.
        table_name (str): The name of the table to update.
        gameid (str): The gameid to update.
        overtime_number (int): The overtime number to increment by.

    Returns:
        None
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"""
                   UPDATE {table_name} 
                   SET overtime_alert_number = overtime_alert_number + 1
                   WHERE gameid = '{gameid}';
                   """)
    connection.commit()
    connection.close()
