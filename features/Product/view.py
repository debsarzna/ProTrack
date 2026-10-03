from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import *
from features.Product.model import Product


class AddProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)

        self.setWindowTitle("Update Product" if product else "Add Product")
        self.setFixedSize(350, 350)

        layout = QVBoxLayout(self)

        name_label = QLabel("Product Name")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")

        price_label = QLabel("Price")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter price")

        quantity_label = QLabel("Quantity")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")

        if product:
            self.name_input.setText(product.name)
            self.price_input.setText(str(product.price))
            self.quantity_input.setText(str(product.quantity))

        submit_button = QPushButton("Update" if product else "Add")
        submit_button.setFixedHeight(40)
        submit_button.clicked.connect(self.validate_and_accept)

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(price_label)
        layout.addWidget(self.price_input)
        layout.addWidget(quantity_label)
        layout.addWidget(self.quantity_input)
        layout.addStretch()
        layout.addWidget(submit_button)

    def validate_and_accept(self):
        name = self.name_input.text().strip()
        price = self.price_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not name or not price or not quantity:
            QMessageBox.warning(self, "Missing information", "Please fill in all fields.")
            return

        try:
            if float(price) < 0:
                raise ValueError
            if int(quantity) < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid input",
                "Price must be a number and quantity must be a whole number, and neither can be negative."
            )
            return

        self.accept()


class ProductPage(QWidget):
    def __init__(self, product_service):
        super().__init__()
        self.product_service = product_service

        layout = QVBoxLayout(self)
        product_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search products...")
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(self.search_products)

        clear_button = QPushButton("Clear")
        clear_button.setFixedWidth(100)
        clear_button.clicked.connect(self.search_input.clear)

        add_button = QPushButton("+ Add")
        add_button.clicked.connect(self.open_add_product)
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

        product_layout.addStretch()
        product_layout.addWidget(self.search_input)
        product_layout.addWidget(clear_button)
        product_layout.addWidget(add_button)
        layout.addLayout(product_layout)



        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setMaximumWidth(600)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(["Name", "Price", "Quantity", "Status"])
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 127)
        layout.addWidget(self.table)

        self.load_products()


        update_button = QPushButton("Update")
        update_button.setFixedWidth(80)
        update_button.setFixedHeight(30)
        update_button.clicked.connect(self.open_update_product)
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
        delete_button.clicked.connect(self.delete_selected_product)
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

    STATUS_COLORS = {
        "In Stock": "#16A34A",  # green
        "Low Stock": "#CA8A04",  # yellow (darker so it's readable on white)
        "Out of Stock": "#DC2626",  # red
    }

    @staticmethod
    def compute_status(quantity: int) -> str:
        if quantity == 0:
            return "Out of Stock"
        if quantity < 10:
            return "Low Stock"
        return "In Stock"

    def open_add_product(self):
        dialog = AddProductDialog(self)
        if dialog.exec():
            quantity = int(dialog.quantity_input.text())
            product = Product(
                name=dialog.name_input.text(),
                price=float(dialog.price_input.text()),
                quantity=quantity,
                status=self.compute_status(quantity),
            )
            self.product_service.add_product(product)
            self.search_products()

    def open_update_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Update", "Select a product first.")
            return

        name_item = self.table.item(row, 0)
        product_id = name_item.data(Qt.ItemDataRole.UserRole)
        current = Product(
            id=product_id,
            name=name_item.text(),
            price=float(self.table.item(row, 1).text().replace(",", "")),
            quantity=int(self.table.item(row, 2).text()),
            status=self.table.item(row, 3).text(),
        )

        dialog = AddProductDialog(self, current)
        if dialog.exec():
            quantity = int(dialog.quantity_input.text())
            updated = Product(
                id=product_id,
                name=dialog.name_input.text(),
                price=float(dialog.price_input.text()),
                quantity=quantity,
                status=self.compute_status(quantity),
            )
            self.product_service.update_product(updated)
            self.search_products()

    def load_products(self, products=None):
        if products is None:
            products = self.product_service.get_product()
        self.table.setRowCount(0)

        for product in products:
            row = self.table.rowCount()
            self.table.insertRow(row)

            name_item = QTableWidgetItem(product.name)
            name_item.setData(Qt.ItemDataRole.UserRole, product.id)
            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, QTableWidgetItem(f"{product.price:,.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(str(product.quantity)))
            status_item = QTableWidgetItem(product.status)
            status_item.setForeground(QColor(self.STATUS_COLORS.get(product.status, "#18181B")))
            self.table.setItem(row, 3, status_item)

    def delete_selected_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Delete", "Select a product first.")
            return

        name_item = self.table.item(row, 0)
        product_id = name_item.data(Qt.ItemDataRole.UserRole)

        answer = QMessageBox.question(
            self, "Confirm delete", f"Delete '{name_item.text()}'?"
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.product_service.delete_product(product_id)
            self.search_products()

    def search_products(self):
        query = self.search_input.text()
        products = self.product_service.search_products(query)
        self.load_products(products)