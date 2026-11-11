"""Product catalog and stock levels."""
 
from __future__ import annotations
 
from orderhub.models import Product
from orderhub.storage import JsonStore
 
 
class ProductNotFound(Exception):
    pass
 
 
class DuplicateProduct(Exception):
    pass
 
 
class CatalogService:
    def __init__(self, store: JsonStore) -> None:
        self.store = store
 
    def add_product(self, sku: str, name: str, price_cents: int, stock: int = 0) -> Product:
        if price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if stock < 0:
            raise ValueError("stock must not be negative")
        data = self.store.load()
        if any(p["sku"] == sku for p in data["products"]):
            raise DuplicateProduct(sku)
        product = Product(sku=sku, name=name, price_cents=price_cents, stock=stock)
        data["products"].append(product.to_dict())
        self.store.save(data)
        return product
 
    def list_products(self) -> list[Product]:
        return [Product.from_dict(p) for p in self.store.load()["products"]]
 
    def get_product(self, sku: str) -> Product:
        for product in self.list_products():
            if product.sku == sku:
                return product
        raise ProductNotFound(sku)
 
    def adjust_stock(self, sku: str, delta: int) -> Product:
        """Add ``delta`` (may be negative) to the stock of a product and save."""
        data = self.store.load()
        for raw in data["products"]:
            if raw["sku"] == sku:
                raw["stock"] = raw.get("stock", 0) + delta
                self.store.save(data)
                return Product.from_dict(raw)
        raise ProductNotFound(sku)
