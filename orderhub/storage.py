"""JSON file storage. The whole database is one small JSON document."""
 
from __future__ import annotations
 
import json
import os
from pathlib import Path
 
DEFAULT_DB = "orderhub.json"
 
 
def default_db_path() -> Path:
    return Path(os.environ.get("ORDERHUB_DB", DEFAULT_DB))
 
 
class JsonStore:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path is not None else default_db_path()
 
    def load(self) -> dict:
        if not self.path.exists():
            return {"products": [], "orders": []}
        with self.path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        data.setdefault("products", [])
        data.setdefault("orders", [])
        return data
 
    def save(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
