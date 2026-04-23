from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: str = ""
    login: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    password_hash: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def from_mongo(doc: dict) -> "User":
        """Создать User из документа MongoDB"""
        return User(
            id=str(doc.get("_id", "")),
            login=doc.get("login", ""),
            first_name=doc.get("first_name", ""),
            last_name=doc.get("last_name", ""),
            email=doc.get("email", ""),
            password_hash=doc.get("password_hash", ""),
            created_at=doc.get("created_at", datetime.now()),
            updated_at=doc.get("updated_at", datetime.now()),
        )

    def to_mongo(self) -> dict:
        """Преобразовать User в документ MongoDB для вставки/обновления"""
        result = {
            "login": self.login,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if self.id:
            result["_id"] = self.id
        return result

    def update_from_mongo(self, doc: dict) -> None:
        """Обновить поля User из документа MongoDB"""
        self.id = str(doc.get("_id", ""))
        self.login = doc.get("login", "")
        self.first_name = doc.get("first_name", "")
        self.last_name = doc.get("last_name", "")
        self.email = doc.get("email", "")
        self.password_hash = doc.get("password_hash", "")
        self.created_at = doc.get("created_at", datetime.now())
        self.updated_at = doc.get("updated_at", datetime.now())
