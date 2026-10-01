# scripts/ingest.py — populate the tracker from configured sources
import logging
from src.aggregate import load_config, collect
from src.store import save_all

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if __name__ == "__main__":
    listings = collect(load_config())                      # fetch, normalize, filter, dedupe
    count = save_all(listings)                             # upsert; existing statuses preserved
    print(f"Saved {count} listings.")