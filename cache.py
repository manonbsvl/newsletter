import hashlib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / "summaries"
CACHE_DIR.mkdir(exist_ok=True)

def _hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()

def get_cached_summary(url: str) -> str | None:
    key = _hash_url(url)
    path = CACHE_DIR / f"{key}.json"

    if not path.exists():
        return None

    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("summary")

def save_summary(url: str, summary: str):
    key = _hash_url(url)
    path = CACHE_DIR / f"{key}.json"

    data = {
        "url": url,
        "summary": summary,
    }

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
