import json                                              # for parsing the model's response
import os
from pathlib import Path
from anthropic import Anthropic                          # official API client
from dotenv import load_dotenv                           # reads .env into the environment
from src.models import Listing

load_dotenv()                                            # must run before reading the key

PROMPT_PATH = Path("prompts/tailor.md")                  # role-specific, editable without code
RESUME_PATH = Path("profile/base_resume.md")             # git-ignored, your real resume
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2000

class TailorError(Exception):
    """Raised when tailoring fails in a way the caller should report, not crash on."""

def _load(path: Path) -> str:
    if not path.exists():
        raise TailorError(f"Missing required file: {path}")
    return path.read_text()

def _client() -> Anthropic:
    key = os.environ.get("ANTHROPIC_API_KEY")            # never hardcode, never log
    if not key:
        raise TailorError("ANTHROPIC_API_KEY not set — copy .env.example to .env")
    return Anthropic(api_key=key)

def _strip_fences(text: str) -> str:
    """Remove a leading ```json fence if the model added one despite instructions."""
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    lines = lines[1:]                                    # drop the opening ``` or ```json
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]                               # drop the closing fence
    return "\n".join(lines).strip()

def tailor(listing: Listing) -> dict:
    """Return tailored bullets and a keyword gap summary for one listing."""
    system_prompt = _load(PROMPT_PATH)
    resume = _load(RESUME_PATH)

    user_content = (                                     # listing wrapped in delimiters
        f"<resume>\n{resume}\n</resume>\n\n"
        f"<listing>\n"
        f"Title: {listing.title}\n"
        f"Company: {listing.company}\n"
        f"Location: {listing.location}\n\n"
        f"{listing.description}\n"
        f"</listing>"
    )

    try:
        response = _client().messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,                        # rules here, above the untrusted listing
            messages=[{"role": "user", "content": user_content}],
        )
    except Exception as exc:                             # network, auth, rate limit
        raise TailorError(f"API call failed: {exc}") from exc

    text = "".join(block.text for block in response.content if block.type == "text").strip()
    text = _strip_fences(text)                           # handle the known formatting quirk

    try:
        return json.loads(text)                          # strict once fences are gone
    except json.JSONDecodeError as exc:
        raise TailorError(                               # show what came back, for diagnosis
            f"Model did not return valid JSON. First 300 chars:\n{text[:300]}"
        ) from exc