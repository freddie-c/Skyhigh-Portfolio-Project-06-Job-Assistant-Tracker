import sqlite3                                           # stdlib, no server, single file
from contextlib import contextmanager
from pathlib import Path
from src.models import Listing
from src.dedupe import _key                              # reuse the dedup identity as the row id

DB_PATH = Path("data/tracker.db")

STATUSES = ["Saved", "Applied", "Interviewing", "Rejected", "Offer"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS listings (
    id           TEXT PRIMARY KEY,                       -- normalized company|title|location
    title        TEXT NOT NULL,
    company      TEXT NOT NULL,
    location     TEXT,
    url          TEXT,
    description  TEXT,
    posted_date  TEXT,                                   -- ISO string; SQLite has no date type
    sources      TEXT,                                   -- comma-joined source names
    status       TEXT NOT NULL DEFAULT 'Saved',          -- survives re-aggregation
    first_seen   TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

@contextmanager
def connect():
    """Open the DB, ensure the schema exists, commit on success, always close."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)     # create data/ on first run
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row                        # rows behave like dicts
    try:
        conn.executescript(SCHEMA)                        # idempotent: IF NOT EXISTS
        yield conn
        conn.commit()
    finally:
        conn.close()

def row_id(listing: Listing) -> str:
    return "|".join(_key(listing))                        # same identity dedupe uses

def upsert(conn, listing: Listing) -> None:
    """Insert a listing, or refresh its fields — but never overwrite status."""
    conn.execute(
        """
        INSERT INTO listings (id, title, company, location, url, description, posted_date, sources)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET                     -- row exists: refresh content only
            title       = excluded.title,
            location    = excluded.location,
            url         = excluded.url,
            description = excluded.description,
            posted_date = excluded.posted_date,
            sources     = excluded.sources,
            updated_at  = datetime('now')
        """,
        (                                                 # parameterized, never f-strings
            row_id(listing),
            listing.title,
            listing.company,
            listing.location,
            listing.url,
            listing.description,
            listing.posted_date.isoformat() if listing.posted_date else None,
            ",".join(listing.sources),
        ),
    )

def save_all(listings: list[Listing]) -> int:
    with connect() as conn:
        for listing in listings:
            upsert(conn, listing)
    return len(listings)

def all_rows() -> list[dict]:
    with connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM listings ORDER BY company, title")]

def set_status(listing_id: str, status: str) -> None:
    if status not in STATUSES:                            # validate before it reaches SQL
        raise ValueError(f"Unknown status: {status}")
    with connect() as conn:
        conn.execute(
            "UPDATE listings SET status = ?, updated_at = datetime('now') WHERE id = ?",
            (status, listing_id),                         # parameterized
        )