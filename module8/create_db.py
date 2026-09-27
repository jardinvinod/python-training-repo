import sqlite3

conn = sqlite3.connect("company.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    position TEXT NOT NULL,
    salary REAL
)
""")

employees = [
    ("John", "Engineering", "Software Engineer", 75000),
    ("Sarah", "HR", "HR Manager", 68000),
    ("David", "Engineering", "Data Engineer", 80000),
    ("Emma", "Finance", "Accountant", 62000),
    ("Michael", "Engineering", "AI Engineer", 90000)
]

cursor.executemany("""
INSERT INTO employees
(name, department, position, salary)
VALUES (?, ?, ?, ?)
""", employees)

conn.commit()
conn.close()

print("Database created successfully.")