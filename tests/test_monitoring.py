
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from monitoring import log_event, LOG_FILE


def test_log_event_writes_valid_json():
    log_event(
        role="hr",
        outcome="answered",
        latency_ms=123.45,
    )

    assert LOG_FILE.exists()

    # Read the latest record written to the log.
    lines = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    event = json.loads(lines[-1])

    assert event["role"] == "hr"
    assert event["outcome"] == "answered"
    assert event["latency_ms"] == 123.45
    assert event["error_type"] is None
    assert "timestamp" in event


def test_log_event_records_blocked_outcome():
    log_event(
        role="general",
        outcome="blocked",
        latency_ms=5.0,
    )

    lines = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    event = json.loads(lines[-1])

    assert event["role"] == "general"
    assert event["outcome"] == "blocked"


def test_log_event_records_error_type():
    log_event(
        role="finance",
        outcome="error",
        latency_ms=50.0,
        error_type="RuntimeError",
    )

    lines = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    event = json.loads(lines[-1])

    assert event["outcome"] == "error"
    assert event["error_type"] == "RuntimeError"



# from monitoring import calculate_estimated_cost_usd
from monitoring import (
    log_event,
    LOG_FILE,
    calculate_estimated_cost_usd,
)

def test_calculate_estimated_cost():
    cost = calculate_estimated_cost_usd(
        prompt_tokens=161,
        completion_tokens=45,
    )

    assert cost == 0.000025575


def test_zero_tokens_have_zero_cost():
    cost = calculate_estimated_cost_usd(
        prompt_tokens=0,
        completion_tokens=0,
    )

    assert cost == 0.0



def test_log_event_records_token_usage_and_cost():
    log_event(
        role="hr",
        outcome="answered",
        latency_ms=100.0,
        prompt_tokens=161,
        completion_tokens=45,
        estimated_cost_usd=calculate_estimated_cost_usd(161, 45),
    )

    lines = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    event = json.loads(lines[-1])

    assert event["prompt_tokens"] == 161
    assert event["completion_tokens"] == 45
    assert event["total_tokens"] == 206
    assert event["estimated_cost_usd"] == 0.000025575
