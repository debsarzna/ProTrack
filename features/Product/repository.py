from database.database import Database
from features.Product.model import Product

class ProductRepository:
    def __init__(self, database: Database):
        self.database = database

    def add(self, product: Product)-> Product:
        with self.database.connect() as con:
            cursor = con.execute(
                """
                INSERT INTO products
                (name, price, quantity, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    product.name,
                    product.price,
                    product.quantity,
                    product.status
                )
            )

            product.id = cursor.lastrowid
        return product

    def list(self) -> list[Product]:
        with self.database.connect() as con:
            rows = con.execute(
                "SELECT id, name, price, quantity, status FROM products"
            ).fetchall()
        return [
            Product(id=row[0], name=row[1], price=row[2],
                    quantity=row[3], status=row[4])
            for row in rows
        ]
    def delete(self, product_id: int) -> None:
        with self.database.connect() as con:
            con.execute("DELETE FROM products WHERE id = ?", (product_id,))

    def search(self, query: str) -> list[Product]:
        with self.database.connect() as con:
            rows = con.execute(
                "SELECT id, name, price, quantity, status FROM products WHERE name LIKE ?",
                (f"%{query}%",)
            ).fetchall()
        return [
            Product(id=row[0], name=row[1], price=row[2],
                    quantity=row[3], status=row[4])
            for row in rows
        ]

    def update(self, product: Product) -> None:
        with self.database.connect() as con:
            con.execute(
                """
                UPDATE products
                SET name = ?, price = ?, quantity = ?, status = ?
                WHERE id = ?
                """,
                (product.name, product.price, product.quantity, product.status, product.id)
            )