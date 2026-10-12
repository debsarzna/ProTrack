from database.database import Database
from features.Product.model import Product, StockMovement
from features.Product.repository import ProductRepository
from features.Dashboard.activity_log import activity_log


class ProductService:
    def __init__(self, database: Database):
        self.repository = ProductRepository(database)

    @staticmethod
    def compute_status(quantity: int) -> str:
        if quantity == 0:
            return "Out of Stock"
        if quantity < 10:
            return "Low Stock"
        return "In Stock"

    def add_product(self, product: Product) -> Product:
        saved = self.repository.add(product)
        if saved.quantity > 0:
            # starting stock shows up in the history as the first Stock In
            self.repository.add_movement(saved.id, "in", saved.quantity, saved.quantity)
        activity_log.add("Added", "Product", product.name)
        return saved

    def get_product(self) -> list[Product]:
        return self.repository.list()

    def get_product_by_id(self, product_id: int) -> Product | None:
        return self.repository.get(product_id)

    def delete_product(self, product_id: int) -> None:
        product = self.repository.get(product_id)
        if product is None:
            raise ValueError("Product not found")
        if product.quantity > 0:
            raise ValueError(
                f"Cannot delete. {product.name} still has {product.quantity} in stock."
            )
        self.repository.delete(product_id)
        activity_log.add("Deleted", "Product", product.name)

    def search_products(self, query: str) -> list[Product]:
        query = query.strip()
        if not query:
            return self.repository.list()
        return self.repository.search(query)

    def update_product(self, product: Product) -> None:
        # name and price only: quantity can only change through stock in / stock out
        existing = self.repository.get(product.id)
        if existing is None:
            raise ValueError("Product not found")
        product.quantity = existing.quantity
        product.status = existing.status
        self.repository.update(product)
        activity_log.add("Updated", "Product", product.name)

    def stock_in(self, product_id: int, amount: int) -> Product:
        return self._move_stock(product_id, "in", amount)

    def stock_out(self, product_id: int, amount: int) -> Product:
        return self._move_stock(product_id, "out", amount)

    def _move_stock(self, product_id: int, movement_type: str, amount: int) -> Product:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        product = self.repository.get(product_id)
        if product is None:
            raise ValueError("Product not found")

        if movement_type == "in":
            new_quantity = product.quantity + amount
        else:
            if amount > product.quantity:
                raise ValueError(f"Not enough stock. Only {product.quantity} available.")
            new_quantity = product.quantity - amount

        new_status = self.compute_status(new_quantity)
        self.repository.record_stock_change(
            product_id, movement_type, amount, new_quantity, new_status
        )
        product.quantity = new_quantity
        product.status = new_status

        if movement_type == "in":
            activity_log.add("Stock In", "Product", f"{product.name} (+{amount})")
        else:
            activity_log.add("Stock Out", "Product", f"{product.name} (-{amount})")
        return product

    def get_movements(self, product_id: int) -> list[StockMovement]:
        return self.repository.list_movements(product_id)