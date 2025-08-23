from typing import Optional


def evaluate(time_ms: int, max_ms: Optional[int] = None) -> dict:
    ok = max_ms is None or time_ms <= max_ms
    return {"time_ms": time_ms, "max_ms": max_ms, "ok": ok}


__all__ = ["evaluate"]
