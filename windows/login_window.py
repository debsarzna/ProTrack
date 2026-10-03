from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)


class loginwindow(QWidget):
    login_success = pyqtSignal(object)  # sends the Employee who logged in

    def __init__(self, employee_service):
        super().__init__()
        self.employee_service = employee_service
        self.setWindowTitle("Login")
        self.setFixedSize(250, 250)
        self.build_ui()
        self.apply_styles()

    def build_ui(self) -> None:
        layout = QVBoxLayout()

        title = QLabel("ProTrack")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addStretch()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.username.setPlaceholderText("Enter Username")
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.username)
        layout.addWidget(self.password)

        login_button = QPushButton("Login")
        login_button.setFixedSize(200, 37)
        login_button.clicked.connect(self.attempt_login)
        self.username.returnPressed.connect(self.attempt_login)
        self.password.returnPressed.connect(self.attempt_login)
        layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def apply_styles(self) -> None:
        self.setStyleSheet("""
            QWidget {
                background-color: #0a1929;
                color: #ffffff;
                font-size: 14px;
            }
            
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #55efc4;
            }
            QLineEdit {
                background-color: #2d3436;
                border: 1px solid #dcdde1;
                border-radius: 6px;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #0984e3;
            }
            QPushButton {
                background-color: #0984e3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0773c5;
            }
            QPushButton:pressed {
                background-color: #065da0;
            }
        """)

    def attempt_login(self) -> None:
        employee = self.employee_service.authenticate(
            self.username.text(), self.password.text()
        )
        if employee is None:
            QMessageBox.warning(self, "Login failed", "Invalid username or password.")
            self.password.clear()
            return
        self.login_success.emit(employee)

    def reset(self) -> None:
        self.username.clear()
        self.password.clear()
        self.username.setFocus()