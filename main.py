import sys
from PyQt6.QtWidgets import QApplication
from database.database import Database
from features.Employee.service import EmployeeService
from windows.login_window import loginwindow
from windows.main_window import mainwindow


def main() -> int:
    app = QApplication(sys.argv)

    database = Database()
    database.create_tables()
    employee_service = EmployeeService(database)
    employee_service.ensure_default_admin()

    login = loginwindow(employee_service)
    state = {"main": None}

    def show_main(employee):
        login.hide()
        state["main"] = mainwindow(database)
        state["main"].logged_out.connect(on_logout)
        state["main"].show()
        login.hide()

    def on_logout():
        state["main"].close()
        state["main"] = None
        login.reset()
        login.show()

    login.login_success.connect(show_main)
    login.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())