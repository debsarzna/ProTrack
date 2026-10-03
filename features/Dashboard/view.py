from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from features.Dashboard.activity_log import activity_log
class Dashboard(QWidget):
    def __init__(self, product_service, employee_service):
        super().__init__()
        self.product_service = product_service
        self.employee_service = employee_service

        layout = QVBoxLayout(self)
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        card_style = """
            QLabel {
                background-color: white;
                color: #18181B;
                border: 1px solid #E4E4E7;
                border-radius: 8px;
                padding: 16px;
                font-size: 16px;
            }
        """


        self.products_label = QLabel()
        self.products_label.setStyleSheet(card_style)
        self.employees_label = QLabel()
        self.employees_label.setStyleSheet(card_style)

        cards_row = QHBoxLayout()
        cards_row.addWidget(self.products_label)
        cards_row.addWidget(self.employees_label)
        layout.addLayout(cards_row)

        self.in_stock_label = QLabel()
        self.low_stock_label = QLabel()
        self.out_of_stock_label = QLabel()

        status_row = QHBoxLayout()
        for label in (self.in_stock_label, self.low_stock_label, self.out_of_stock_label):
            label.setStyleSheet(card_style)
            status_row.addWidget(label)
        layout.addLayout(status_row)

        layout.addStretch()

        activity_title = QLabel("Recent Activity")
        activity_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(activity_title)

        self.activity_table = QTableWidget(0, 3)
        self.activity_table.setHorizontalHeaderLabels(["Action", "Type", "Details"])
        self.activity_table.verticalHeader().setVisible(False)
        self.activity_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.activity_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.activity_table.setAlternatingRowColors(True)
        self.activity_table.setShowGrid(False)
        self.activity_table.horizontalHeader().setStretchLastSection(True)
        self.activity_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.activity_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.activity_table, 1)

        self.refresh()

    def refresh(self):
        products = self.product_service.get_product()
        employees = self.employee_service.get_employees()

        in_stock = sum(1 for p in products if p.status == "In Stock")
        low_stock = sum(1 for p in products if p.status == "Low Stock")
        out_of_stock = sum(1 for p in products if p.status == "Out of Stock")

        self.products_label.setText(f"Total Products\n{len(products)}")
        self.employees_label.setText(f"Total Employees\n{len(employees)}")
        self.in_stock_label.setText(f"In Stock\n{in_stock}")
        self.low_stock_label.setText(f"Low Stock\n{low_stock}")
        self.out_of_stock_label.setText(f"Out of Stock\n{out_of_stock}")
        self.load_activity()

    def load_activity(self):
        entries = activity_log.recent(10)
        self.activity_table.setRowCount(len(entries))
        for row, entry in enumerate(entries):
            for col, value in enumerate(entry):
                self.activity_table.setItem(row, col, QTableWidgetItem(str(value)))

    def showEvent(self, event):
        self.refresh()
        super().showEvent(event)