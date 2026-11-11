"""Command line interface: ``python -m orderhub <command>``."""
 
from __future__ import annotations
 
import argparse
import sys
 
from orderhub.catalog import CatalogService, DuplicateProduct, ProductNotFound
from orderhub.orders import InsufficientStock, OrderNotFound, OrderService
from orderhub.storage import JsonStore
 
 
def format_money(cents: int) -> str:
    return f"{cents / 100:.2f}"
 
 
def parse_money(text: str) -> int:
    return int(round(float(text) * 100))
 
 
def parse_item(text: str) -> tuple[str, int]:
    sku, _, quantity = text.partition(":")
    return sku, int(quantity or 1)
 
 
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orderhub", description="Small order management tool")
    parser.add_argument("--db", help="path to the JSON database file")
    sub = parser.add_subparsers(dest="command", required=True)
 
    product = sub.add_parser("product", help="manage products").add_subparsers(
        dest="action", required=True
    )
    add = product.add_parser("add", help="add a product")
    add.add_argument("sku")
    add.add_argument("name")
    add.add_argument("price", help="price such as 12.50")
    add.add_argument("stock", type=int)
    product.add_parser("list", help="list products")
 
    order = sub.add_parser("order", help="manage orders").add_subparsers(
        dest="action", required=True
    )
    create = order.add_parser("create", help="place an order")
    create.add_argument("customer")
    create.add_argument("items", nargs="+", help="items as SKU:QTY, for example PEN-01:3")
    order.add_parser("list", help="list orders")
    cancel = order.add_parser("cancel", help="cancel an order")
    cancel.add_argument("order_id", type=int)
    return parser
 
 
def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = JsonStore(args.db)
    catalog = CatalogService(store)
    orders = OrderService(store, catalog)
 
    try:
        if args.command == "product" and args.action == "add":
            product = catalog.add_product(
                args.sku, args.name, parse_money(args.price), args.stock
            )
            print(f"Added {product.sku} ({product.name})")
        elif args.command == "product" and args.action == "list":
            for product in catalog.list_products():
                print(
                    f"{product.sku:<10} {product.name:<24} "
                    f"{format_money(product.price_cents):>8}  stock={product.stock}"
                )
        elif args.command == "order" and args.action == "create":
            order = orders.create_order(args.customer, [parse_item(i) for i in args.items])
            total = format_money(order.total_cents)
            print(f"Order {order.id} placed for {order.customer}: {total}")
        elif args.command == "order" and args.action == "list":
            for order in orders.list_orders():
                print(
                    f"#{order.id:<4} {order.customer:<16} {order.status:<10} "
                    f"{format_money(order.total_cents):>8}"
                )
        elif args.command == "order" and args.action == "cancel":
            order = orders.cancel_order(args.order_id)
            print(f"Order {order.id} is {order.status}")
    except (ProductNotFound, OrderNotFound) as exc:
        print(f"Not found: {exc}", file=sys.stderr)
        return 1
    except (DuplicateProduct, InsufficientStock, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
