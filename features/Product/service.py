from database.database import Database
from features.Product.model import Product
from features.Product.repository import ProductRepository
from features.Dashboard.activity_log import activity_log

class ProductService:
    def __init__(self, database: Database):
        self.repository = ProductRepository(database)

    def add_product(self, product: Product) -> Product:
        saved = self.repository.add(product)
        activity_log.add("Added", "Product", product.name)
        return saved
    def get_product(self) -> list[Product]:
        return self.repository.list()

    def delete_product(self, product_id: int) -> None:
        self.repository.delete(product_id)
        activity_log.add("Deleted", "Product", f"ID {product_id}")

    def search_products(self, query: str) -> list[Product]:
        query = query.strip()
        if not query:
            return self.repository.list()
        return self.repository.search(query)

    def update_product(self, product: Product) -> None:
        self.repository.update(product)
        activity_log.add("Updated", "Product", product.name)