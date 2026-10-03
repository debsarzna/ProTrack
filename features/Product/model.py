from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    quantity: int
    status: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")