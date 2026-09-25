import requests

API_BASE = "https://api.lever.co/v0/postings"             # public postings API, no auth

def fetch(company: str, timeout: int = 10) -> list[dict]:
    """Return raw posting dicts for one Lever board. Raises on failure."""
    response = requests.get(
        f"{API_BASE}/{company}",
        params={"mode": "json"},                          # JSON instead of the HTML board
        timeout=timeout,                                  # same no-hang rule as Greenhouse
    )
    response.raise_for_status()                           # let the orchestrator decide to skip
    return response.json()                                # Lever returns a bare list, not a dict