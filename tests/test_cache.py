"""Tests for the SQLite response cache"""

from pathlib import Path

from llmcost.cache import CachedResponse, ResponseCache, make_key

MODEL = "claude-sonnet-5-5"
RESPONSE = CachedResponse(text="Hello", input_tokens=10, output_tokens=10)


def test_same_request_gives_same_key() -> None:
    key_a = make_key(MODEL, "Hi", max_tokens=100)
    key_b = make_key(MODEL, "Hi", max_tokens=100)
    assert key_a == key_b
    assert len(key_a) == 64


def test_different_prompt_gives_different_key() -> None:
    assert make_key(MODEL, "Hi", max_tokens=100) != make_key(MODEL, "Hello", max_tokens=100)


def test_different_model_gives_different_key() -> None:
    assert make_key(MODEL, "Hi", max_tokens=100) != make_key("other", "Hi", max_tokens=100)


def test_get_missing_key_returns_none(tmp_path: Path) -> None:
    cache = ResponseCache(tmp_path / "cache.db")
    assert cache.get("no-such-key") is None


def test_put_then_get_returns_same_response(tmp_path: Path) -> None:
    cache = ResponseCache(tmp_path / "cache.db")
    cache.put("k1", RESPONSE)
    assert cache.get("k1") == RESPONSE


def test_cache_survives_reopen(tmp_path: Path) -> None:
    db_path = tmp_path / "cache.db"
    ResponseCache(db_path).put("k1", RESPONSE)
    assert ResponseCache(db_path).get("k1") == RESPONSE


def test_put_same_key_twice_keeps_latest(tmp_path: Path) -> None:
    cache = ResponseCache(tmp_path / "cache.db")
    cache.put("k1", RESPONSE)
    newer = CachedResponse(text="Updated", input_tokens=1, output_tokens=1)
    cache.put("k1", newer)
    assert cache.get("k1") == newer
