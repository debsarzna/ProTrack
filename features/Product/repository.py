from database.database import Database
from features.Product.model import Product, StockMovement


class ProductRepository:
    def __init__(self, database: Database):
        self.database = database

    def _to_product(self, row) -> Product:
        return Product(id=row[0], name=row[1], price=row[2],
                       quantity=row[3], status=row[4])

    def add(self, product: Product) -> Product:
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
        return [self._to_product(row) for row in rows]

    def get(self, product_id: int) -> Product | None:
        with self.database.connect() as con:
            row = con.execute(
                "SELECT id, name, price, quantity, status FROM products WHERE id = ?",
                (product_id,)
            ).fetchone()
        return self._to_product(row) if row else None

    def delete(self, product_id: int) -> None:
        with self.database.connect() as con:
            con.execute("DELETE FROM stock_movements WHERE product_id = ?", (product_id,))
            con.execute("DELETE FROM products WHERE id = ?", (product_id,))

    def search(self, query: str) -> list[Product]:
        with self.database.connect() as con:
            rows = con.execute(
                "SELECT id, name, price, quantity, status FROM products WHERE name LIKE ?",
                (f"%{query}%",)
            ).fetchall()
        return [self._to_product(row) for row in rows]

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

    def add_movement(self, product_id: int, movement_type: str,
                     amount: int, quantity_after: int) -> None:
        with self.database.connect() as con:
            con.execute(
                """
                INSERT INTO stock_movements
                (product_id, movement_type, amount, quantity_after)
                VALUES (?, ?, ?, ?)
                """,
                (product_id, movement_type, amount, quantity_after)
            )

    def record_stock_change(self, product_id: int, movement_type: str, amount: int,
                            new_quantity: int, new_status: str) -> None:
        # one connection = one transaction: the quantity and the history row
        # are saved together or not at all
        with self.database.connect() as con:
            con.execute(
                "UPDATE products SET quantity = ?, status = ? WHERE id = ?",
                (new_quantity, new_status, product_id)
            )
            con.execute(
                """
                INSERT INTO stock_movements
                (product_id, movement_type, amount, quantity_after)
                VALUES (?, ?, ?, ?)
                """,
                (product_id, movement_type, amount, new_quantity)
            )

    def list_movements(self, product_id: int, limit: int = 100) -> list[StockMovement]:
        with self.database.connect() as con:
            rows = con.execute(
                """
                SELECT id, product_id, movement_type, amount, quantity_after, created_at
                FROM stock_movements
                WHERE product_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (product_id, limit)
            ).fetchall()
        return [StockMovement(*row) for row in rows]