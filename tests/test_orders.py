import pytest
 
from orderhub.orders import InsufficientStock, OrderNotFound
 
 
def test_create_order_reduces_stock(orders, catalog):
    order = orders.create_order("Asha", [("PEN-01", 2), ("NOTE-01", 1)])
    assert order.id == 1
    assert order.total_cents == 2 * 150 + 499
    assert catalog.get_product("PEN-01").stock == 8
    assert catalog.get_product("NOTE-01").stock == 4
 
 
def test_order_rejected_when_stock_too_low(orders):
    with pytest.raises(InsufficientStock):
        orders.create_order("Ravi", [("NOTE-01", 99)])
 
 
def test_cancel_restores_stock(orders, catalog):
    order = orders.create_order("Asha", [("PEN-01", 4)])
    cancelled = orders.cancel_order(order.id)
    assert cancelled.status == "cancelled"
    assert catalog.get_product("PEN-01").stock == 10
 
 
def test_list_orders_by_status(orders):
    first = orders.create_order("Asha", [("PEN-01", 1)])
    orders.create_order("Ravi", [("PEN-01", 1)])
    orders.cancel_order(first.id)
    assert [o.customer for o in orders.list_orders(status="placed")] == ["Ravi"]
 
 
def test_unknown_order(orders):
    with pytest.raises(OrderNotFound):
        orders.get_order(42)
