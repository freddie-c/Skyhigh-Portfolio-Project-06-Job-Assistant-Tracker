import logging
import yaml
from src.fetchers import greenhouse
from src.normalize import from_greenhouse
from src.models import Listing
from src.dedupe import dedupe

log = logging.getLogger(__name__)

FETCHERS = {                                          # type -> (fetch fn, normalize fn)
    "greenhouse": (greenhouse.fetch, from_greenhouse),
}

def load_config(path: str = "sources.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)                      # safe_load, never load()

def matches(title: str, filters: dict) -> bool:
    """Title passes if it hits an include term and no exclude term."""
    lowered = title.lower()
    include = filters.get("include", [])
    exclude = filters.get("exclude", [])
    if include and not any(term in lowered for term in include):
        return False
    return not any(term in lowered for term in exclude)

def collect(config: dict) -> list[Listing]:
    """Run every configured source. A dead source is logged and skipped."""
    filters = config.get("filters", {})
    results: list[Listing] = []

    for source in config.get("sources", []):
        name = source.get("name", "?")
        fetcher = FETCHERS.get(source.get("type"))
        if fetcher is None:
            log.warning("Unknown source type for %s — skipping", name)
            continue

        fetch_fn, normalize_fn = fetcher
        try:
            raw_jobs = fetch_fn(source["board_token"])          # network call
        except Exception as exc:                                # dead source, timeout, 404
            log.warning("Source %s failed (%s) — skipping", name, exc)
            continue                                            # other sources still run

        for job in raw_jobs:
            try:
                if not matches(job.get("title", ""), filters):  # cheap check before parsing
                    continue
                results.append(normalize_fn(job, name))
            except Exception as exc:                            # one bad record, not a dead run
                log.warning("Could not normalize a job from %s (%s)", name, exc)

        log.info("Source %s returned %d raw jobs", name, len(raw_jobs))

    return dedupe(results)
