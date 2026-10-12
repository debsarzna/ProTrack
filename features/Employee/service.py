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
    def __init__(self, database: Database, current_user: Employee | None = None):
        self.repository = EmployeeRepository(database)
        self.current_user = current_user   # None for the pre-login instance

    @property
    def is_admin(self) -> bool:
        return self.current_user is not None and self.current_user.role == "admin"

    def _require_admin(self) -> None:
        if not self.is_admin:
            raise PermissionError("Only admin accounts can manage employees.")

    def _visible(self, employees: list[Employee]) -> list[Employee]:
        if self.is_admin:
            return employees
        return [e for e in employees if e.role != "admin"]

    def _verify_current_user_password(self, password: str, message: str) -> None:
        if self.current_user is None:
            raise PermissionError("Not logged in.")
        stored = self.repository.get_by_username(self.current_user.username)
        if stored is None or not verify_password(password, stored.password_hash):
            raise ValueError(message)

    def add_employee(self, first_name: str, username: str, password: str) -> Employee:
        self._require_admin()
        if not password:
            raise ValueError("Password is required")
        employee = Employee(
            first_name=first_name,
            username=username,
            password_hash=hash_password(password),
            role="employee",
        )
        try:
            saved = self.repository.add(employee)
        except sqlite3.IntegrityError:
            raise ValueError("That username is already taken")
        activity_log.add("Added", "Employee", first_name)
        return saved

    def get_employees(self) -> list[Employee]:
        return self._visible(self.repository.list())

    def search_employees(self, query: str) -> list[Employee]:
        query = query.strip()
        if not query:
            return self.get_employees()
        return self._visible(self.repository.search(query))

    def update_employee(self, original_username: str, employee: Employee,
                        new_password: str = "", current_password: str = "") -> None:
        if self.current_user is None:
            raise PermissionError("Not logged in.")
        if not self.is_admin and original_username != self.current_user.username:
            raise PermissionError("You can only edit your own account.")
        if new_password:
            if not self.is_admin:
                self._verify_current_user_password(current_password, "Your password is incorrect")
            employee.password_hash = hash_password(new_password)
        try:
            self.repository.update(original_username, employee)
        except sqlite3.IntegrityError:
            raise ValueError("That username is already taken")
        if original_username == self.current_user.username:
            self.current_user.username = employee.username  # renamed their own account
        activity_log.add("Updated", "Employee", employee.username)

    def change_own_password(self, old_password: str, new_password: str) -> None:
        if not new_password:
            raise ValueError("New password is required")
        self._verify_current_user_password(old_password, "Old password is incorrect")
        stored = self.repository.get_by_username(self.current_user.username)
        stored.password_hash = hash_password(new_password)
        self.repository.update(stored.username, stored)
        activity_log.add("Updated", "Employee", stored.username)

    def delete_employee(self, username: str) -> None:
        self._require_admin()
        if username == self.current_user.username:
            raise ValueError("You can't delete your own account.")
        self.repository.delete(username)
        activity_log.add("Deleted", "Employee", username)

    def authenticate(self, username: str, password: str) -> Employee | None:
        employee = self.repository.get_by_username(username.strip())
        if employee and verify_password(password, employee.password_hash):
            return employee
        return None

    def ensure_default_admin(self, username: str = "admin", password: str = "admin123") -> None:
        if self.repository.get_by_username(username) is None:
            self.repository.add(Employee(
                first_name="Admin",
                username=username,
                password_hash=hash_password(password),
                role="admin",
            ))
            activity_log.add("Added", "Employee", "Admin")