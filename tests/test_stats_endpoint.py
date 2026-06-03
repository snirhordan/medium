"""Tests for GET /api/stats endpoint against the RAG assignment specification."""
import os

import pytest
import requests

BASE_URL = os.environ.get("RAG_BASE_URL", "http://localhost:3000")
STATS_URL = f"{BASE_URL.rstrip('/')}/api/stats"
REQUIRED_FIELDS = {"chunk_size", "overlap_ratio", "top_k"}


def _fetch_stats():
    try:
        return requests.get(STATS_URL, timeout=10)
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Could not reach {STATS_URL}: {exc}")


@pytest.fixture(scope="session")
def stats_response():
    """Session-scoped fixture: GET /api/stats once and reuse for all tests."""
    return _fetch_stats()


def test_stats_returns_200_and_json(stats_response):
    """Spec: endpoint must respond 200 with JSON body."""
    assert stats_response.status_code == 200, (
        f"Expected 200, got {stats_response.status_code}: {stats_response.text!r}"
    )
    content_type = stats_response.headers.get("content-type", "")
    assert "application/json" in content_type.lower(), (
        f"Expected application/json content-type, got {content_type!r}"
    )


def test_stats_response_has_only_required_fields(stats_response):
    """Spec: 'Strict JSON format (must match exactly these field names)' -- enforce exact key set."""
    body = stats_response.json()
    assert isinstance(body, dict), f"Expected JSON object, got {type(body).__name__}"
    assert set(body.keys()) == REQUIRED_FIELDS, (
        f"Expected exactly {REQUIRED_FIELDS}, got {set(body.keys())}"
    )


def test_stats_chunk_size_is_integer_within_1024_cap(stats_response):
    """Spec: chunk_size is integer; assignment caps chunks at 1024 tokens."""
    body = stats_response.json()
    chunk_size = body["chunk_size"]
    assert isinstance(chunk_size, int) and not isinstance(chunk_size, bool), (
        f"chunk_size must be int (not bool/float), got {type(chunk_size).__name__}"
    )
    assert 1 <= chunk_size <= 1024, f"chunk_size {chunk_size} not in [1, 1024]"


def test_stats_overlap_ratio_in_range(stats_response):
    """Spec: overlap_ratio is a number between 0 and 0.3 (inclusive)."""
    body = stats_response.json()
    overlap_ratio = body["overlap_ratio"]
    assert isinstance(overlap_ratio, (int, float)) and not isinstance(overlap_ratio, bool), (
        f"overlap_ratio must be a number (not bool), got {type(overlap_ratio).__name__}"
    )
    assert 0 <= overlap_ratio <= 0.3, f"overlap_ratio {overlap_ratio} not in [0, 0.3]"


def test_stats_top_k_in_range(stats_response):
    """Spec: top_k is integer between 1 and 30."""
    body = stats_response.json()
    top_k = body["top_k"]
    assert isinstance(top_k, int) and not isinstance(top_k, bool), (
        f"top_k must be int (not bool), got {type(top_k).__name__}"
    )
    assert 1 <= top_k <= 30, f"top_k {top_k} not in [1, 30]"


def test_stats_idempotent(stats_response):
    """Spec: endpoint must always reflect current values -- two back-to-back GETs must agree."""
    second = _fetch_stats()
    assert second.status_code == 200, (
        f"Second GET expected 200, got {second.status_code}: {second.text!r}"
    )
    assert stats_response.json() == second.json(), (
        "Two consecutive GETs returned different JSON bodies"
    )
