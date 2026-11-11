import pytest
 
from orderhub.catalog import DuplicateProduct, ProductNotFound
 
 
def test_add_and_list_products(catalog):
    skus = [p.sku for p in catalog.list_products()]
    assert skus == ["PEN-01", "NOTE-01"]
 
 
def test_duplicate_sku_is_rejected(catalog):
    with pytest.raises(DuplicateProduct):
        catalog.add_product("PEN-01", "Another pen", 100)
 
 
def test_get_unknown_product(catalog):
    with pytest.raises(ProductNotFound):
        catalog.get_product("NOPE")
 
 
def test_adjust_stock(catalog):
    assert catalog.adjust_stock("PEN-01", -3).stock == 7
    assert catalog.get_product("PEN-01").stock == 7
