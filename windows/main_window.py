from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import *
from features.Product.view import ProductPage
from features.Product.service import ProductService
from features.Employee.view import EmployeePage
from features.Employee.service import EmployeeService
from features.Dashboard.view import Dashboard
class mainwindow(QMainWindow):
    logged_out = pyqtSignal()

    def __init__(self, database):
        super().__init__()
        self.database = database
        self.setWindowTitle("Main Window")
        self.setFixedSize(761, 500)
        self.build_ui()

    def build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(150)
        sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #18181B;
            }
        """)
        sidebar = QVBoxLayout(sidebar_widget)

        dashboard_button = QPushButton("Dashboard")
        sidebar.addWidget(dashboard_button)

        employee_button = QPushButton("Employee")
        sidebar.addWidget(employee_button)

        products_button = QPushButton("Products")
        sidebar.addWidget(products_button)

        sidebar.addStretch()

        logout_button = QPushButton("Logout")
        sidebar.addWidget(logout_button)

        product_service = ProductService(self.database)
        employee_service = EmployeeService(self.database)

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


    def show_dashboard(self):
        self.dashboard_page.refresh()
        self.pages_layout.setCurrentIndex(0)


