import sqlite3
from pathlib import Path
from mcp.server import MCPServer


# ---------------------------------------------------------
# MCP SERVER
# ---------------------------------------------------------

mcp = MCPServer("Employee Database MCP Server")


# ---------------------------------------------------------
# DATABASE PATH
# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "company.db"


# ---------------------------------------------------------
# DATABASE CREATION
# ---------------------------------------------------------

def create_database():
    """
    Create the SQLite database and employees table
    if they do not already exist.
    """

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)

    # Check whether data already exists
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]

    # Insert sample data only if table is empty
    if count == 0:
        employees = [
            ("John Smith", "Engineering", "Software Engineer", 75000),
            ("Sarah Johnson", "HR", "HR Manager", 68000),
            ("David Lee", "Engineering", "Data Engineer", 80000),
            ("Emma Brown", "Finance", "Accountant", 62000),
            ("Michael Wilson", "Engineering", "AI Engineer", 90000),
            ("Anna Thomas", "Sales", "Sales Executive", 65000)
        ]

        cursor.executemany("""
            INSERT INTO employees
            (name, department, position, salary)
            VALUES (?, ?, ?, ?)
        """, employees)

    conn.commit()
    conn.close()


# Create database when server starts
create_database()


# ---------------------------------------------------------
# MCP TOOL 1
# GET ALL EMPLOYEES
# ---------------------------------------------------------

@mcp.tool()
def get_all_employees() -> list[dict]:
    """
    Return all employees stored in the SQLite database.
    """

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, department, position, salary
        FROM employees
        ORDER BY id
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ---------------------------------------------------------
# MCP TOOL 2
# GET EMPLOYEE BY ID
# ---------------------------------------------------------

@mcp.tool()
def get_employee(employee_id: int) -> dict:
    """
    Return an employee using the employee ID.
    """

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, department, position, salary
        FROM employees
        WHERE id = ?
    """, (employee_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {
            "error": f"No employee found with ID {employee_id}"
        }

    return dict(row)


# ---------------------------------------------------------
# MCP TOOL 3
# GET EMPLOYEES BY DEPARTMENT
# ---------------------------------------------------------

@mcp.tool()
def get_employees_by_department(department: str) -> list[dict]:
    """
    Return all employees belonging to a given department.
    """

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, department, position, salary
        FROM employees
        WHERE LOWER(department) = LOWER(?)
        ORDER BY name
    """, (department,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ---------------------------------------------------------
# MCP TOOL 4
# GET ALL DEPARTMENTS
# ---------------------------------------------------------

@mcp.tool()
def get_departments() -> list[str]:
    """
    Return all unique departments.
    """

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT department
        FROM employees
        ORDER BY department
    """)

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]


# ---------------------------------------------------------
# MCP TOOL 5
# SEARCH EMPLOYEE BY NAME
# ---------------------------------------------------------

@mcp.tool()
def search_employee(name: str) -> list[dict]:
    """
    Search employees whose names contain the supplied text.
    """

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, department, position, salary
        FROM employees
        WHERE LOWER(name) LIKE LOWER(?)
        ORDER BY name
    """, (f"%{name}%",))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ---------------------------------------------------------
# MCP TOOL 6
# GET EMPLOYEE COUNT
# ---------------------------------------------------------

@mcp.tool()
def get_employee_count() -> dict:
    """
    Return the total number of employees.
    """

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM employees
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return {
        "total_employees": count
    }


# ---------------------------------------------------------
# START MCP SERVER
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run()