
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "monitoring.jsonl"

logger = logging.getLogger("enterprise_rag")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)



def log_event(
    role: str,
    outcome: str,
    latency_ms: float | None = None,
    error_type: str | None = None,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    estimated_cost_usd: float | None = None,
) -> None:
    """Log operational metadata without storing question or answer text."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "role": role,
        "outcome": outcome,
        "latency_ms": (
            round(latency_ms, 2) if latency_ms is not None else None
        ),
        "error_type": error_type,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": (
            prompt_tokens + completion_tokens
            if prompt_tokens is not None and completion_tokens is not None
            else None
        ),
        "estimated_cost_usd": estimated_cost_usd,
    }

    logger.info(json.dumps(event))



def calculate_estimated_cost_usd(
    prompt_tokens: int,
    completion_tokens: int,
) -> float:
    """Estimate Groq API cost for GPT-OSS 20B using standard token rates."""
    input_price_per_million = 0.075
    output_price_per_million = 0.30

    input_cost = prompt_tokens * input_price_per_million / 1_000_000
    output_cost = completion_tokens * output_price_per_million / 1_000_000

    return round(input_cost + output_cost, 12)
