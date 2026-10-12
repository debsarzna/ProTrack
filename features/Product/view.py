from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import *
from features.Product.model import Product

STATUS_COLORS = {
    "In Stock": "#16A34A",
    "Low Stock": "#CA8A04",
    "Out of Stock": "#DC2626",
}


class AddProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.is_edit = product is not None

        self.setWindowTitle("Update Product" if self.is_edit else "Add Product")
        self.setFixedSize(350, 260)

        layout = QVBoxLayout(self)

        name_label = QLabel("Product Name")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")

        price_label = QLabel("Price")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter price")

        if product:
            self.name_input.setText(product.name)
            self.price_input.setText(str(product.price))

        submit_button = QPushButton("Update" if self.is_edit else "Add")
        submit_button.setFixedHeight(40)
        submit_button.clicked.connect(self.validate_and_accept)

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(price_label)
        layout.addWidget(self.price_input)
        layout.addStretch()
        layout.addWidget(submit_button)

    def validate_and_accept(self):
        name = self.name_input.text().strip()
        price = self.price_input.text().strip()

        if not name or not price:
            QMessageBox.warning(self, "Missing information", "Please fill in all fields.")
            return

        try:
            if float(price) < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid input",
                "Price must be a number and cannot be negative."
            )
            return

        self.accept()


class StockDialog(QDialog):
    def __init__(self, parent, product_service, product_id):
        super().__init__(parent)
        self.product_service = product_service
        self.product_id = product_id

        self.setWindowTitle("Stock In / Stock Out")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout(self)

        self.name_label = QLabel()
        self.name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.stock_label = QLabel()

        amount_label = QLabel("Amount")
        self.amount_input = QSpinBox()
        self.amount_input.setRange(1, 1_000_000)
        self.amount_input.setValue(1)
        self.amount_input.setFixedHeight(30)

        stock_in_button = QPushButton("Stock In")
        stock_in_button.setFixedHeight(36)
        stock_in_button.clicked.connect(lambda: self.move_stock("in"))
        stock_in_button.setStyleSheet("""
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

        stock_out_button = QPushButton("Stock Out")
        stock_out_button.setFixedHeight(36)
        stock_out_button.clicked.connect(lambda: self.move_stock("out"))
        stock_out_button.setStyleSheet("""
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
        button_row.addWidget(stock_in_button)
        button_row.addWidget(stock_out_button)

        history_label = QLabel("History")
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Date", "Type", "Amount", "Balance"])
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        close_button = QPushButton("Close")
        close_button.setFixedHeight(36)
        close_button.clicked.connect(self.accept)

        layout.addWidget(self.name_label)
        layout.addWidget(self.stock_label)
        layout.addWidget(amount_label)
        layout.addWidget(self.amount_input)
        layout.addLayout(button_row)
        layout.addWidget(history_label)
        layout.addWidget(self.history_table)
        layout.addWidget(close_button)

        self.refresh()

    def refresh(self):
        product = self.product_service.get_product_by_id(self.product_id)
        if product is None:
            return

        self.name_label.setText(product.name)
        color = STATUS_COLORS.get(product.status, "#18181B")
        self.stock_label.setText(
            f"Current stock: <b>{product.quantity}</b> &nbsp;|&nbsp; "
            f"<span style='color:{color};'>{product.status}</span>"
        )

        movements = self.product_service.get_movements(self.product_id)
        self.history_table.setRowCount(0)
        for movement in movements:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)

            is_in = movement.movement_type == "in"
            type_item = QTableWidgetItem("Stock In" if is_in else "Stock Out")
            amount_item = QTableWidgetItem(
                f"+{movement.amount}" if is_in else f"-{movement.amount}"
            )
            tint = QColor("#16A34A" if is_in else "#DC2626")
            type_item.setForeground(tint)
            amount_item.setForeground(tint)

            self.history_table.setItem(row, 0, QTableWidgetItem(movement.created_at[:10]))
            self.history_table.setItem(row, 1, type_item)
            self.history_table.setItem(row, 2, amount_item)
            self.history_table.setItem(row, 3, QTableWidgetItem(str(movement.quantity_after)))

    def move_stock(self, movement_type: str):
        amount = self.amount_input.value()
        try:
            if movement_type == "in":
                self.product_service.stock_in(self.product_id, amount)
            else:
                self.product_service.stock_out(self.product_id, amount)
        except ValueError as e:
            QMessageBox.warning(self, "Cannot update stock", str(e))
            return
        self.amount_input.setValue(1)
        self.refresh()


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
        # double-click a product to open its stock in / stock out window
        self.table.cellDoubleClicked.connect(lambda *_: self.open_stock_dialog())
        layout.addWidget(self.table)

        self.load_products()

        stock_button = QPushButton("Stock")
        stock_button.setFixedWidth(80)
        stock_button.setFixedHeight(30)
        stock_button.clicked.connect(self.open_stock_dialog)
        stock_button.setStyleSheet("""
            QPushButton {
                background-color: #7C3AED;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #6D28D9;
            }
        """)

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
        button_row.addWidget(stock_button)
        button_row.addWidget(update_button)
        button_row.addWidget(delete_button)
        layout.addLayout(button_row)

    def open_add_product(self):
        dialog = AddProductDialog(self)
        if dialog.exec():
            # new products start empty; use Stock In to add stock
            product = Product(
                name=dialog.name_input.text(),
                price=float(dialog.price_input.text()),
                quantity=0,
                status=self.product_service.compute_status(0),
            )
            self.product_service.add_product(product)
            self.search_products()

    def open_stock_dialog(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Stock", "Select a product first.")
            return

        product_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        dialog = StockDialog(self, self.product_service, product_id)
        dialog.exec()
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
            updated = Product(
                id=product_id,
                name=dialog.name_input.text(),
                price=float(dialog.price_input.text()),
                quantity=current.quantity,   # unchanged: the service keeps the stored quantity
                status=current.status,
            )
            try:
                self.product_service.update_product(updated)
            except ValueError as e:
                QMessageBox.warning(self, "Cannot update product", str(e))
                return
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
            status_item.setForeground(QColor(STATUS_COLORS.get(product.status, "#18181B")))
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
            try:
                self.product_service.delete_product(product_id)
            except ValueError as e:
                QMessageBox.warning(self, "Cannot delete product", str(e))
                return
            self.search_products()

    def search_products(self):
        query = self.search_input.text()
        products = self.product_service.search_products(query)
        self.load_products(products)