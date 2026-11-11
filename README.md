# OrderHub
 
OrderHub is a small order management service for a stationery shop.
It is the sample repository for the course
**Orchestration Fundamentals for Agentic Development**.
 
## Quick start
 
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```
 
## Usage
 
```bash
python -m orderhub product add PEN-01 "Blue pen" 1.50 100
python -m orderhub product add NOTE-01 "Notebook A5" 4.99 40
python -m orderhub product list
python -m orderhub order create Asha PEN-01:3 NOTE-01:1
python -m orderhub order list
python -m orderhub order cancel 1
```
 
Data is stored in `orderhub.json` (override with `--db` or `ORDERHUB_DB`).
 
## Quality checks
 
```bash
pytest          # tests
ruff check .    # lint
```
 
See `docs/architecture.md` for the module layout.
