from database.database import Database
from features.Employee.model import Employee


class EmployeeRepository:
    def __init__(self, database: Database):
        self.database = database

    def _to_employee(self, row) -> Employee:
        return Employee(first_name=row[0], username=row[1], password_hash=row[2])

    def add(self, employee: Employee) -> Employee:
        with self.database.connect() as con:
            con.execute(
                """
                INSERT INTO employees (username, first_name, password_hash)
                VALUES (?, ?, ?)
                """,
                (employee.username, employee.first_name, employee.password_hash)
            )
        return employee

    def list(self) -> list[Employee]:
        with self.database.connect() as con:
            rows = con.execute(
                "SELECT first_name, username, password_hash FROM employees"
            ).fetchall()
        return [self._to_employee(row) for row in rows]

    def search(self, query: str) -> list[Employee]:
        like = f"%{query}%"
        with self.database.connect() as con:
            rows = con.execute(
                """
                SELECT first_name, username, password_hash
                FROM employees
                WHERE first_name LIKE ? OR username LIKE ?
                """,
                (like, like)
            ).fetchall()
        return [self._to_employee(row) for row in rows]

    def get_by_username(self, username: str) -> Employee | None:
        with self.database.connect() as con:
            row = con.execute(
                "SELECT first_name, username, password_hash FROM employees WHERE username = ?",
                (username,)
            ).fetchone()
        return self._to_employee(row) if row else None

    def update(self, original_username: str, employee: Employee) -> None:
        with self.database.connect() as con:
            con.execute(
                """
                UPDATE employees
                SET first_name = ?, username = ?, password_hash = ?
                WHERE username = ?
                """,
                (employee.first_name, employee.username,
                 employee.password_hash, original_username)
            )

    def delete(self, username: str) -> None:
        with self.database.connect() as con:
            con.execute("DELETE FROM employees WHERE username = ?", (username,))