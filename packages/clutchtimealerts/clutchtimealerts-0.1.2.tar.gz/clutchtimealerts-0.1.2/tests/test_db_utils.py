import pytest
import sqlite3
from clutchtimealerts.db_utils import (
    TABLE_NAME,
    EXPECTED_COLUMNS,
    check_and_recreate_table,
    clear_table,
    insert_game,
    update_alert_sent,
    check_alert_sent,
    check_overtime_alert_sent,
    update_overtime_number,
)
import tempfile
import os


@pytest.fixture
def db_name():
    """Fixture to create a fresh instance of NotificationCollector."""
    temp_file = tempfile.NamedTemporaryFile()
    temp_file_name = temp_file.name
    print(temp_file_name)
    return temp_file_name


def test_check_and_recreate_table(db_name):
    """Test that the table is created with the expected schema."""

    check_and_recreate_table(db_name, TABLE_NAME, EXPECTED_COLUMNS)

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Get the schema of the table
    cursor.execute(f"PRAGMA table_info({TABLE_NAME});")
    data = cursor.fetchall()
    connection.close()
    schema = []
    for row in data:
        row_name = row[1]
        row_type = row[2]
        not_null = " NOT NULL" if row[3] else ""
        default_value = f" DEFAULT {row[4]}" if row[4] else ""
        primary_key = " PRIMARY KEY" if row[5] else ""

        schema.append((row_name, f"{row_type}{not_null}{default_value}{primary_key}"))

    assert schema == EXPECTED_COLUMNS
    connection.close()


def test_insert_game(db_name):
    """Test inserting a new game."""
    check_and_recreate_table(db_name, TABLE_NAME, EXPECTED_COLUMNS)

    gameid = "0022400205"
    insert_game(db_name, TABLE_NAME, gameid)

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT gameid FROM {TABLE_NAME} WHERE gameid = '{gameid}';")
    result = cursor.fetchone()
    connection.close()

    assert result is not None
    assert result[0] == gameid


def test_update_alert_sent(db_name):
    """Test updating the alert_sent column."""
    check_and_recreate_table(db_name, TABLE_NAME, EXPECTED_COLUMNS)

    # Check initial alerts is 0
    gameid = "0022400205"
    insert_game(db_name, TABLE_NAME, gameid)
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT alert_sent FROM {TABLE_NAME} WHERE gameid = '{gameid}';")
    result = cursor.fetchone()
    connection.close()

    assert result[0] == 0

    # Test updated alert
    update_alert_sent(db_name, TABLE_NAME, gameid)

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT alert_sent FROM {TABLE_NAME} WHERE gameid = '{gameid}';")
    result = cursor.fetchone()
    connection.close()

    assert result[0] == 1


def test_check_alert_sent(db_name):
    """Test checking the alert_sent status."""
    check_and_recreate_table(db_name, TABLE_NAME, EXPECTED_COLUMNS)
    gameid = "0022400205"
    insert_game(db_name, TABLE_NAME, gameid)
    assert not check_alert_sent(db_name, TABLE_NAME, gameid)

    update_alert_sent(db_name, TABLE_NAME, gameid)
    assert check_alert_sent(db_name, TABLE_NAME, gameid)


def test_check_overtime_alert_sent(db_name):
    """Test checking the overtime_alert_number status."""
    check_and_recreate_table(db_name, TABLE_NAME, EXPECTED_COLUMNS)
    gameid = "0022400205"
    insert_game(db_name, TABLE_NAME, gameid)

    assert not check_overtime_alert_sent(db_name, TABLE_NAME, gameid, 1)

    update_overtime_number(db_name, TABLE_NAME, gameid)
    assert not check_overtime_alert_sent(db_name, TABLE_NAME, gameid, 0)
    assert check_overtime_alert_sent(db_name, TABLE_NAME, gameid, 1)

    update_overtime_number(db_name, TABLE_NAME, gameid)
    assert not check_overtime_alert_sent(db_name, TABLE_NAME, gameid, 1)
    assert check_overtime_alert_sent(db_name, TABLE_NAME, gameid, 2)


def test_update_overtime_number(db_name):
    """Test incrementing the overtime_alert_number."""
    check_and_recreate_table(db_name, TABLE_NAME, EXPECTED_COLUMNS)
    gameid = "0022400205"
    insert_game(db_name, TABLE_NAME, gameid)

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT overtime_alert_number FROM {TABLE_NAME} WHERE gameid = '{gameid}';"
    )
    result = cursor.fetchone()
    connection.close()

    assert result[0] == 0

    update_overtime_number(db_name, TABLE_NAME, gameid)
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT overtime_alert_number FROM {TABLE_NAME} WHERE gameid = '{gameid}';"
    )
    result = cursor.fetchone()
    connection.close()

    assert result[0] == 1

    update_overtime_number(db_name, TABLE_NAME, gameid)
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT overtime_alert_number FROM {TABLE_NAME} WHERE gameid = '{gameid}';"
    )
    result = cursor.fetchone()
    connection.close()

    assert result[0] == 2


def test_clear_table(db_name):
    """Test clearing the table."""
    check_and_recreate_table(db_name, TABLE_NAME, EXPECTED_COLUMNS)
    gameid = "0022400205"
    insert_game(db_name, TABLE_NAME, gameid)

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME};")
    result = cursor.fetchall()
    connection.close()

    assert len(result) == 1

    clear_table(db_name, TABLE_NAME)

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME};")
    result = cursor.fetchall()
    connection.close()

    assert len(result) == 0
