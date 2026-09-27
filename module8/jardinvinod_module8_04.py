import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "knowledge.db"


def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    """Create the SQLite database and table."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            information TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_information(name: str, category: str, information: str):
    """Insert information into the database."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO information (name, category, information)
        VALUES (?, ?, ?)
        """,
        (name, category, information)
    )

    connection.commit()

    record_id = cursor.lastrowid

    connection.close()

    return record_id


def get_all_information():
    """Return all stored information."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, category, information
        FROM information
        ORDER BY id
    """)

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_information_by_id(record_id: int):
    """Return one database record."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, category, information
        FROM information
        WHERE id = ?
        """,
        (record_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def search_information(search_text: str):
    """Search records."""

    connection = get_connection()
    cursor = connection.cursor()

    search_pattern = f"%{search_text}%"

    cursor.execute(
        """
        SELECT id, name, category, information
        FROM information
        WHERE name LIKE ?
           OR category LIKE ?
           OR information LIKE ?
        ORDER BY id
        """,
        (
            search_pattern,
            search_pattern,
            search_pattern
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def delete_information(record_id: int):
    """Delete a database record."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM information
        WHERE id = ?
        """,
        (record_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted > 0


create_database()