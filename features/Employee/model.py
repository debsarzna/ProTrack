from dataclasses import dataclass


@dataclass
class Employee:
    first_name: str
    username: str
    password_hash: str

    def __post_init__(self) -> None:
        self.first_name = self.first_name.strip()
        self.username = self.username.strip()
        if not self.first_name:
            raise ValueError("First name is required")
        if not self.username:
            raise ValueError("Username is required")