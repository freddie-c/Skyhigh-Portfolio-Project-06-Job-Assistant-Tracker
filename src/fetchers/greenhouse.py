import requests                                          # HTTP client from your venv

API_BASE = "https://boards-api.greenhouse.io/v1/boards"  # public board API, no auth

def fetch(board_token: str, timeout: int = 10) -> list[dict]:
    """Return raw job dicts for one Greenhouse board. Raises on failure."""
    url = f"{API_BASE}/{board_token}/jobs"                # same URL your curl loop used
    response = requests.get(
        url,
        params={"content": "true"},                      # include the description field
        timeout=timeout,                                 # never hang forever on a dead host
    )
    response.raise_for_status()                           # turn 404/500 into an exception
    return response.json().get("jobs", [])                # .get = empty list, not KeyError