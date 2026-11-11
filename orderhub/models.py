"""Data models for OrderHub. Money is always stored as integer cents."""
 
from __future__ import annotations
 
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
 
 
def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
 
 
@dataclass
class Product:
    sku: str
    name: str
    price_cents: int
    stock: int = 0
 
    def to_dict(self) -> dict:
        return asdict(self)
 
    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(
            sku=data["sku"],
            name=data["name"],
            price_cents=data["price_cents"],
            stock=data.get("stock", 0),
        )
 
 
@dataclass
class OrderLine:
    sku: str
    quantity: int
    unit_price_cents: int
 
    @property
    def line_total_cents(self) -> int:
        return self.quantity * self.unit_price_cents
 
 
@dataclass
class Order:
    id: int
    customer: str
    lines: list[OrderLine] = field(default_factory=list)
    status: str = "placed"  # placed | cancelled
    created_at: str = field(default_factory=_now)
 
    @property
    def total_cents(self) -> int:
        return sum(line.line_total_cents for line in self.lines)
 
    def to_dict(self) -> dict:
        return asdict(self)
 
    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        return cls(
            id=data["id"],
            customer=data["customer"],
            lines=[OrderLine(**line) for line in data.get("lines", [])],
            status=data.get("status", "placed"),
            created_at=data.get("created_at", _now()),
        )
