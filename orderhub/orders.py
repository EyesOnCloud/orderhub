"""Placing, listing and cancelling orders."""
 
from __future__ import annotations
 
from orderhub.catalog import CatalogService
from orderhub.models import Order, OrderLine
from orderhub.storage import JsonStore
 
 
class InsufficientStock(Exception):
    pass
 
 
class OrderNotFound(Exception):
    pass
 
 
class OrderService:
    def __init__(self, store: JsonStore, catalog: CatalogService) -> None:
        self.store = store
        self.catalog = catalog
 
    def create_order(self, customer: str, items: list[tuple[str, int]]) -> Order:
        """Place an order. ``items`` is a list of ``(sku, quantity)`` pairs."""
        if not customer.strip():
            raise ValueError("customer must not be empty")
        if not items:
            raise ValueError("an order needs at least one item")
 
        lines: list[OrderLine] = []
        for sku, quantity in items:
            if quantity <= 0:
                raise ValueError("quantity must be positive")
            product = self.catalog.get_product(sku)
            if product.stock < quantity:
                raise InsufficientStock(f"{sku}: wanted {quantity}, have {product.stock}")
            self.catalog.adjust_stock(sku, -quantity)
            lines.append(
                OrderLine(sku=sku, quantity=quantity, unit_price_cents=product.price_cents)
            )
 
        data = self.store.load()
        order = Order(id=len(data["orders"]) + 1, customer=customer.strip(), lines=lines)
        data["orders"].append(order.to_dict())
        self.store.save(data)
        return order
 
    def list_orders(self, status: str | None = None) -> list[Order]:
        orders = [Order.from_dict(o) for o in self.store.load()["orders"]]
        if status is not None:
            orders = [o for o in orders if o.status == status]
        return orders
 
    def get_order(self, order_id: int) -> Order:
        for order in self.list_orders():
            if order.id == order_id:
                return order
        raise OrderNotFound(order_id)
 
    def cancel_order(self, order_id: int) -> Order:
        """Cancel a placed order and put its items back into stock."""
        order = self.get_order(order_id)
        if order.status == "cancelled":
            return order
        for line in order.lines:
            self.catalog.adjust_stock(line.sku, line.quantity)
        data = self.store.load()
        for raw in data["orders"]:
            if raw["id"] == order_id:
                raw["status"] = "cancelled"
        self.store.save(data)
        return self.get_order(order_id)
