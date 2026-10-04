from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
)


class loginwindow(QWidget):
    login_success = pyqtSignal(object)

    def __init__(self, employee_service):
        super().__init__()
        self.employee_service = employee_service
        self.setWindowTitle("ProTrack - Login")
        self.setFixedSize(330, 410)
        self.build_ui()
        self.apply_styles()

    def build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)

        title = QLabel("ProTrack")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Welcome back!")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hint = QLabel("Sign in to continue")
        hint.setObjectName("hint")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(hint)
        layout.addSpacing(25)

        username_label = QLabel("Username")
        username_label.setObjectName("fieldLabel")
        password_label = QLabel("Password")
        password_label.setObjectName("fieldLabel")

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.username.setFixedHeight(42)
        self.password.setFixedHeight(42)

        layout.addWidget(username_label)
        layout.addWidget(self.username)
        layout.addSpacing(6)
        layout.addWidget(password_label)
        layout.addWidget(self.password)
        layout.addStretch()

        exit_button = QPushButton("Exit")
        exit_button.setObjectName("exit")
        exit_button.setFixedHeight(42)
        exit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_button.clicked.connect(self.close)

        login_button = QPushButton("Login")
        login_button.setFixedHeight(42)
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.setDefault(True)
        login_button.clicked.connect(self.attempt_login)
        self.username.returnPressed.connect(self.attempt_login)
        self.password.returnPressed.connect(self.attempt_login)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        button_row.addWidget(exit_button)
        button_row.addWidget(login_button)
        layout.addLayout(button_row)

        self.setLayout(layout)

    def apply_styles(self) -> None:
        self.setStyleSheet("""
            QWidget {
                background-color: #0a1929;
                color: #ffffff;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
                font-size: 14px;
            }

            QLabel#title {
                font-size: 34px;
                font-weight: bold;
                color: #55efc4;
                letter-spacing: 1px;
            }
            QLabel#subtitle {
                font-size: 20px;
                font-weight: 600;
                color: #ffffff;
            }
            QLabel#hint {
                font-size: 13px;
                color: #8fa3b8;
            }
            QLabel#fieldLabel {
                font-size: 12px;
                font-weight: 600;
                color: #8fa3b8;
            }

            QLineEdit {
                background-color: #132f4c;
                border: 1px solid #1e4976;
                border-radius: 8px;
                padding: 0 12px;
                selection-background-color: #0984e3;
            }
            QLineEdit:hover {
                border: 1px solid #2f6fa8;
            }
            QLineEdit:focus {
                border: 1px solid #55efc4;
                background-color: #173a5e;
            }

            QPushButton {
                background-color: #0984e3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0773c5;
            }
            QPushButton:pressed {
                background-color: #065da0;
            }

            QPushButton#exit {
                background-color: transparent;
                border: 1px solid #1e4976;
                color: #c5d3e0;
            }
            QPushButton#exit:hover {
                background-color: #7F1D1D;
                border: 1px solid #7F1D1D;
                color: white;
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
