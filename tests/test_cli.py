from orderhub.cli import main, parse_item, parse_money
 
 
def test_parse_helpers():
    assert parse_money("12.50") == 1250
    assert parse_item("PEN-01:3") == ("PEN-01", 3)
    assert parse_item("PEN-01") == ("PEN-01", 1)
 
 
def test_end_to_end(tmp_path, capsys):
    db = str(tmp_path / "db.json")
    assert main(["--db", db, "product", "add", "PEN-01", "Blue pen", "1.50", "10"]) == 0
    assert main(["--db", db, "order", "create", "Asha", "PEN-01:2"]) == 0
    assert main(["--db", db, "order", "list"]) == 0
    out = capsys.readouterr().out
    assert "Order 1 placed for Asha: 3.00" in out
    assert "#1" in out
 
 
def test_error_exit_code(tmp_path, capsys):
    db = str(tmp_path / "db.json")
    assert main(["--db", db, "order", "cancel", "7"]) == 1
    assert "Not found" in capsys.readouterr().err
