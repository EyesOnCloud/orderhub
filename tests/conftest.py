import pytest
 
from orderhub.catalog import CatalogService
from orderhub.orders import OrderService
from orderhub.storage import JsonStore
 
 
@pytest.fixture
def store(tmp_path):
    return JsonStore(tmp_path / "db.json")
 
 
@pytest.fixture
def catalog(store):
    service = CatalogService(store)
    service.add_product("PEN-01", "Blue pen", 150, stock=10)
    service.add_product("NOTE-01", "Notebook A5", 499, stock=5)
    return service
 
 
@pytest.fixture
def orders(store, catalog):
    return OrderService(store, catalog)
