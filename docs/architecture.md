# OrderHub architecture
 
```
cli.py  ->  orders.py   ->  catalog.py  ->  storage.py  ->  orderhub.json
                \-> models.py <-/
```
 
| Module       | Responsibility                                      |
|--------------|-----------------------------------------------------|
| `models.py`  | `Product`, `OrderLine`, `Order` dataclasses         |
| `storage.py` | Load and save the single JSON database file         |
| `catalog.py` | Products and stock levels                           |
| `orders.py`  | Create, list and cancel orders                      |
| `cli.py`     | `python -m orderhub ...` commands                   |
 
Rules of the codebase:
 
- Money is integer cents everywhere. Convert only at the CLI edge.
- Services never print. Only `cli.py` prints.
- Every behaviour change needs a test in `tests/`.
