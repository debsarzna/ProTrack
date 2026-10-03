from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from features.Employee.model import Employee


class EmployeeDialog(QDialog):

    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.is_edit = employee is not None

        self.setWindowTitle("Update Employee" if self.is_edit else "Add Employee")
        self.setFixedSize(350, 350)

        layout = QVBoxLayout(self)

        first_name_label = QLabel("Name")
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter Name")

        username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")

        password_label = QLabel("New Password" if self.is_edit else "Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText(
            "Leave blank to keep current password" if self.is_edit else "Enter password"
        )

        if employee:
            self.first_name_input.setText(employee.first_name)
            self.username_input.setText(employee.username)

        submit_button = QPushButton("Update" if self.is_edit else "Add")
        submit_button.setFixedHeight(40)
        submit_button.clicked.connect(self.validate_and_accept)

        layout.addWidget(first_name_label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addStretch()
        layout.addWidget(submit_button)

    def validate_and_accept(self):
        first_name = self.first_name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not first_name or not username:
            QMessageBox.warning(self, "Missing information",
                                "Name and username are required.")
            return

        if not self.is_edit and not password:
            QMessageBox.warning(self, "Missing information", "Password is required.")
            return

        self.accept()


class EmployeePage(QWidget):
    def __init__(self, employee_service):
        super().__init__()
        self.employee_service = employee_service

        layout = QVBoxLayout(self)
        top_row = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search employees...")
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(self.search_employees)

        clear_button = QPushButton("Clear")
        clear_button.setFixedWidth(100)
        clear_button.clicked.connect(self.search_input.clear)

        add_button = QPushButton("+ Add")
        add_button.clicked.connect(self.open_add_employee)
        add_button.setFixedWidth(80)
        add_button.setFixedHeight(25)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #16A34A;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #15803D;
            }
        """)

        top_row.addStretch()
        top_row.addWidget(self.search_input)
        top_row.addWidget(clear_button)
        top_row.addWidget(add_button)
        layout.addLayout(top_row)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setMaximumWidth(600)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(["Name", "Username"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        layout.addWidget(self.table)

        update_button = QPushButton("Update")
        update_button.setFixedWidth(80)
        update_button.setFixedHeight(30)
        update_button.clicked.connect(self.open_update_employee)
        update_button.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)

        delete_button = QPushButton("Delete")
        delete_button.setFixedWidth(80)
        delete_button.setFixedHeight(30)
        delete_button.clicked.connect(self.delete_selected_employee)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(update_button)
        button_row.addWidget(delete_button)
        layout.addLayout(button_row)

        self.load_employees()

    def load_employees(self, employees=None):
        if employees is None:
            employees = self.employee_service.get_employees()
        self.table.setRowCount(0)

        for employee in employees:
            row = self.table.rowCount()
            self.table.insertRow(row)

            first_name_item = QTableWidgetItem(employee.first_name)
            # keep the full Employee (incl. password hash) on the row for updates
            first_name_item.setData(Qt.ItemDataRole.UserRole, employee)
            self.table.setItem(row, 0, first_name_item)
            self.table.setItem(row, 1, QTableWidgetItem(employee.username))

    def _selected_employee(self, action: str):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, action, "Select an employee first.")
            return None
        return self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)

    def open_add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec():
            try:
                self.employee_service.add_employee(
                    first_name=dialog.first_name_input.text(),
                    username=dialog.username_input.text(),
                    password=dialog.password_input.text(),
                )
            except ValueError as e:
                QMessageBox.warning(self, "Cannot add employee", str(e))
                return
            self.search_employees()

    def open_update_employee(self):
        current = self._selected_employee("Update")
        if current is None:
            return

        dialog = EmployeeDialog(self, current)
        if dialog.exec():
            try:
                updated = Employee(
                    first_name=dialog.first_name_input.text(),
                    username=dialog.username_input.text(),
                    password_hash=current.password_hash,
                )
                self.employee_service.update_employee(
                    current.username, updated, dialog.password_input.text()
                )
            except ValueError as e:
                QMessageBox.warning(self, "Cannot update employee", str(e))
                return
            self.search_employees()

    def delete_selected_employee(self):
        current = self._selected_employee("Delete")
        if current is None:
            return

        answer = QMessageBox.question(
            self, "Confirm delete", f"Delete '{current.username}'?"
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.employee_service.delete_employee(current.username)
            self.search_employees()

    def search_employees(self):
        employees = self.employee_service.search_employees(self.search_input.text())
        self.load_employees(employees)