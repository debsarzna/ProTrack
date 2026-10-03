import hashlib
import os
import sqlite3
import hmac
from features.Dashboard.activity_log import activity_log
from database.database import Database
from features.Employee.model import Employee
from features.Employee.repository import EmployeeRepository


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return f"{salt.hex()}:{digest.hex()}"
def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, digest_hex = stored_hash.split(":")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except ValueError:
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return hmac.compare_digest(actual, expected)

class EmployeeService:
    def __init__(self, database: Database):
        self.repository = EmployeeRepository(database)

    def add_employee(self, first_name: str, username: str, password: str) -> Employee:
        if not password:
            raise ValueError("Password is required")
        employee = Employee(
            first_name=first_name,
            username=username,
            password_hash=hash_password(password),
        )
        try:
            saved = self.repository.add(employee)
        except sqlite3.IntegrityError:
            raise ValueError("That username is already taken")
        activity_log.add("Added", "Employee", first_name)
        return saved

    def get_employees(self) -> list[Employee]:
        return self.repository.list()

    def search_employees(self, query: str) -> list[Employee]:
        query = query.strip()
        if not query:
            return self.repository.list()
        return self.repository.search(query)

    def update_employee(self, original_username: str, employee: Employee,
                        new_password: str = "") -> None:
        if new_password:
            employee.password_hash = hash_password(new_password)
        try:
            self.repository.update(original_username, employee)
        except sqlite3.IntegrityError:
            raise ValueError("That username is already taken")
        activity_log.add("Updated", "Employee", employee.username)

    def delete_employee(self, username: str) -> None:
        self.repository.delete(username)
        activity_log.add("Deleted", "Employee", username)

    def authenticate(self, username: str, password: str) -> Employee | None:
        employee = self.repository.get_by_username(username.strip())
        if employee and verify_password(password, employee.password_hash):
            return employee
        return None

    def ensure_default_admin(self, username: str = "admin", password: str = "admin123") -> None:
        if self.repository.get_by_username(username) is None:
            self.add_employee("Admin", username, password)