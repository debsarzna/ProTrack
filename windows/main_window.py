from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import *
from features.Product.view import ProductPage
from features.Product.service import ProductService
from features.Employee.view import EmployeePage
from features.Employee.service import EmployeeService
from features.Dashboard.view import Dashboard


class mainwindow(QMainWindow):
    logged_out = pyqtSignal()

    def __init__(self, database, current_user):
        super().__init__()
        self.database = database
        self.current_user = current_user
        self.setWindowTitle("ProTrack")
        self.setFixedSize(761, 500)
        self.build_ui()

    def build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(120)
        sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #18181B;
            }
            QPushButton {
                background-color: transparent;
                color: #E4E4E7;
                border: none;
                border-radius: 6px;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #27272A;
                color: white;
            }
            QPushButton:pressed {
                background-color: #3F3F46;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar_widget)

        dashboard_button = QPushButton("Dashboard")
        employee_button = QPushButton("Employee")
        products_button = QPushButton("Products")
        logout_button = QPushButton("Logout")

        for b in (dashboard_button, employee_button,
                  products_button, logout_button):
            sidebar_layout.addWidget(b)

        sidebar_layout.addStretch()

        product_service = ProductService(self.database)
        employee_service = EmployeeService(self.database, self.current_user)
        self.employee_service = employee_service

        self.pages_layout = QStackedWidget()
        self.dashboard_page = Dashboard(product_service, employee_service)
        employee_page = EmployeePage(employee_service)
        product_page = ProductPage(product_service)
        self.pages_layout.addWidget(self.dashboard_page)
        self.pages_layout.addWidget(employee_page)
        self.pages_layout.addWidget(product_page)

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.pages_layout)

        dashboard_button.clicked.connect(lambda: self.pages_layout.setCurrentIndex(0))
        employee_button.clicked.connect(lambda: self.pages_layout.setCurrentIndex(1))
        products_button.clicked.connect(lambda: self.pages_layout.setCurrentIndex(2))
        logout_button.clicked.connect(self.logged_out.emit)