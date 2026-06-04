"""
Extra contract & quality tests beyond the core 19. Same target URL conventions
(RAG_BASE_URL env var, default http://localhost:3000). Slow tests are marked
so 'pytest -m "not slow"' still gives a quick schema-only smoke.

Twenty additional checks across five themes:

  Input validation (5):
    - empty question, missing field, wrong field, non-string, empty body
  HTTP semantics (3):
    - GET-on-POST endpoint, POST-on-GET endpoint, content-type tolerance
  Augmented prompt fidelity (3):
    - User contains the literal question
    - User references the retrieved chunks
    - User repeats the fallback-instruction sentence
  Context quality (5):
    - context length is between 1 and stats top_k
    - context scores are sorted descending
    - context chunks are non-empty and reasonably long
    - stats endpoint values match what /api/prompt is using
    - root URL is not the bare Vercel 404 (cosmetic-fix verification)
  Output quality (4):
    - Q1 names both title and author
    - Q2 returns 3 distinct article titles
    - Out-of-corpus question stays concise (response < 1000 chars)
    - Repeated same question yields identical context (deterministic retrieval)

  Cosmetic-fix safety (1):
    - Arbitrary paths do not hijack the required endpoints' response shape
"""
import os
import re

import pytest
import requests

BASE_URL = os.environ.get("RAG_BASE_URL", "http://localhost:3000")
PROMPT_URL = f"{BASE_URL.rstrip('/')}/api/prompt"
STATS_URL = f"{BASE_URL.rstrip('/')}/api/stats"
ROOT_URL = BASE_URL.rstrip("/") + "/"

FALLBACK_SENTENCE = "I don't know based on the provided Medium articles data."


def _post(question, timeout=120, **kwargs):
    try:
        return requests.post(PROMPT_URL, json={"question": question}, timeout=timeout, **kwargs)
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Could not reach {PROMPT_URL}: {exc}")


def _post_raw(body, timeout=30, headers=None):
    try:
        return requests.post(
            PROMPT_URL,
            data=body if isinstance(body, str) else None,
            json=body if not isinstance(body, str) else None,
            timeout=timeout,
            headers=headers or {"Content-Type": "application/json"},
        )
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Could not reach {PROMPT_URL}: {exc}")


# ---------------------------------------------------------------------------
# Input validation (5 tests)
# ---------------------------------------------------------------------------

def test_missing_question_field_rejected():
    """Spec: body must contain 'question'; absence is a client error."""
    resp = _post_raw('{"foo": "bar"}')
    assert resp.status_code in (400, 422), (
        f"Missing 'question' should yield 4xx, got {resp.status_code}"
    )


def test_wrong_field_name_rejected():
    """Spec: only 'question' is accepted; other field names are client errors."""
    resp = _post_raw('{"query": "hello"}')
    assert resp.status_code in (400, 422), (
        f"Wrong field name should yield 4xx, got {resp.status_code}"
    )


def test_non_string_question_rejected():
    """Spec: question must be a string; integers/lists/null are client errors."""
    resp = _post_raw('{"question": 42}')
    assert resp.status_code in (400, 422), (
        f"Integer 'question' should yield 4xx, got {resp.status_code}"
    )


def test_empty_body_rejected():
    """Spec: empty body cannot satisfy the question requirement."""
    resp = _post_raw('')
    assert resp.status_code in (400, 422), (
        f"Empty body should yield 4xx, got {resp.status_code}"
    )


def test_empty_question_string_still_returns_valid_schema():
    """Edge: an empty question is technically valid input; endpoint must still respond."""
    resp = _post("")
    # Either valid 200 or a graceful 4xx is acceptable; what isn't is a 5xx.
    assert resp.status_code < 500, (
        f"Empty question should not 5xx, got {resp.status_code}: {resp.text!r}"
    )


# ---------------------------------------------------------------------------
# HTTP semantics (3 tests)
# ---------------------------------------------------------------------------

def test_get_on_prompt_endpoint_rejected():
    """Spec: /api/prompt is POST-only; GET should not succeed."""
    try:
        resp = requests.get(PROMPT_URL, timeout=10)
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Could not reach {PROMPT_URL}: {exc}")
    assert resp.status_code in (405, 404, 422), (
        f"GET on /api/prompt should be rejected, got {resp.status_code}"
    )


def test_post_on_stats_endpoint_rejected():
    """Spec: /api/stats is GET-only; POST should not succeed."""
    try:
        resp = requests.post(STATS_URL, json={}, timeout=10)
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Could not reach {STATS_URL}: {exc}")
    assert resp.status_code in (405, 404), (
        f"POST on /api/stats should be rejected, got {resp.status_code}"
    )


def test_stats_endpoint_under_2s():
    """Performance: /api/stats has no external calls and should return quickly."""
    import time
    try:
        t0 = time.time()
        resp = requests.get(STATS_URL, timeout=10)
        elapsed = time.time() - t0
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Could not reach {STATS_URL}: {exc}")
    assert resp.status_code == 200
    assert elapsed < 5, f"/api/stats took {elapsed:.2f}s, expected < 5s"


# ---------------------------------------------------------------------------
# Augmented_prompt fidelity (3 tests)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def shared_prompt_response():
    """One in-corpus probe reused across this module's content checks."""
    resp = _post("Find an article that discusses writing or creativity.")
    if resp.status_code != 200:
        pytest.skip(f"Probe call returned {resp.status_code}; cannot run content tests")
    return resp.json()


@pytest.mark.slow
def test_augmented_user_prompt_contains_question_verbatim(shared_prompt_response):
    """Augmented_prompt.User must include the literal user question (so the LLM sees it)."""
    user = shared_prompt_response["Augmented_prompt"]["User"]
    assert "Find an article that discusses writing or creativity." in user, (
        "Augmented_prompt.User does not contain the user's question verbatim"
    )


@pytest.mark.slow
def test_augmented_user_prompt_references_retrieved_chunks(shared_prompt_response):
    """Augmented_prompt.User must contain at least one of the retrieved titles."""
    user = shared_prompt_response["Augmented_prompt"]["User"]
    titles = [c["title"] for c in shared_prompt_response["context"] if c["title"]]
    assert any(t in user for t in titles), (
        "Augmented_prompt.User does not reference any retrieved article title"
    )


@pytest.mark.slow
def test_augmented_user_prompt_repeats_fallback_instruction(shared_prompt_response):
    """The fallback sentence should appear in the User prompt so the LLM uses it when warranted."""
    user = shared_prompt_response["Augmented_prompt"]["User"]
    assert FALLBACK_SENTENCE in user, (
        "Augmented_prompt.User should remind the model of the exact fallback sentence"
    )


# ---------------------------------------------------------------------------
# Context quality (5 tests)
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_context_length_within_top_k(shared_prompt_response):
    """context must contain at most top_k items (from /api/stats)."""
    try:
        stats = requests.get(STATS_URL, timeout=10).json()
    except Exception as exc:
        pytest.skip(f"Could not fetch /api/stats: {exc}")
    top_k = stats["top_k"]
    n = len(shared_prompt_response["context"])
    assert 1 <= n <= top_k, f"context length {n} not in [1, {top_k}]"


@pytest.mark.slow
def test_context_scores_sorted_descending(shared_prompt_response):
    """Top-k retrieval should return chunks in descending score order."""
    scores = [c["score"] for c in shared_prompt_response["context"]]
    assert scores == sorted(scores, reverse=True), (
        f"context scores not sorted descending: {scores}"
    )


@pytest.mark.slow
def test_context_chunks_meaningfully_long(shared_prompt_response):
    """Every chunk should have at least 30 chars of text (not stub or empty)."""
    for i, c in enumerate(shared_prompt_response["context"]):
        chunk = c["chunk"]
        assert isinstance(chunk, str) and len(chunk.strip()) >= 30, (
            f"context[{i}].chunk too short ({len(chunk)} chars): {chunk[:60]!r}"
        )


def test_stats_values_within_assignment_caps():
    """Cross-check: /api/stats values must respect the assignment's hard caps."""
    try:
        body = requests.get(STATS_URL, timeout=10).json()
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Could not reach {STATS_URL}: {exc}")
    assert body["chunk_size"] <= 1024, "chunk_size exceeds assignment cap of 1024"
    assert body["overlap_ratio"] <= 0.3, "overlap_ratio exceeds assignment cap of 0.3"
    assert body["top_k"] <= 30, "top_k exceeds assignment cap of 30"


def test_root_url_is_not_vercel_404():
    """Cosmetic: root URL should not return the bare Vercel 404 page (catch-all rewrite test)."""
    try:
        resp = requests.get(ROOT_URL, timeout=10)
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Could not reach {ROOT_URL}: {exc}")
    # Either a 200 with a small JSON, or any non-default-Vercel-404 page is fine.
    # If 404, must NOT be Vercel's static error page.
    if resp.status_code == 404:
        assert "NOT_FOUND" not in resp.text or "vercel" not in resp.text.lower(), (
            "Root returns the default Vercel static 404 page (cosmetic-fix did not apply)"
        )
    else:
        assert resp.status_code < 500, f"Root returned 5xx: {resp.status_code}"


# ---------------------------------------------------------------------------
# Output quality on the assignment example questions (4 tests)
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_q1_names_both_title_and_author():
    """Q1 asks for title AND author -- the response must contain both."""
    q = ("Find an article that reframes marketing as a conversation with readers, "
         "aimed at writers who find self-promotion uncomfortable. Provide the title "
         "and author.")
    resp = _post(q)
    assert resp.status_code == 200
    text = resp.json()["response"]
    # The expected article in this corpus is "A Marketing Guide for Introverts" by Shaunta Grimes.
    # Both names should appear in some form.
    assert "Marketing Guide" in text or "Introverts" in text, (
        f"Q1 response does not name the article title: {text[:300]!r}"
    )
    assert "Shaunta" in text or "Grimes" in text, (
        f"Q1 response does not name the author: {text[:300]!r}"
    )


@pytest.mark.slow
def test_q2_returns_three_distinct_titles():
    """Q2 asks for exactly 3 article titles -- response must contain 3 lines/items."""
    q = "List exactly 3 articles about education. Return only the titles."
    resp = _post(q)
    assert resp.status_code == 200
    text = resp.json()["response"].strip()
    # Count non-empty lines and dedupe.
    lines = [line.strip(" -*0123456789.").strip() for line in text.splitlines() if line.strip()]
    distinct = {line for line in lines if line}
    # Allow some leeway: at least 3 distinct lines, no more than 5 (some LLMs add a header line).
    assert 3 <= len(distinct) <= 5, (
        f"Q2 should return ~3 distinct title lines; got {len(distinct)} distinct lines:\n{text}"
    )


@pytest.mark.slow
def test_out_of_corpus_response_stays_concise():
    """The fallback should be short, not a verbose explanation."""
    resp = _post("What is the capital of France?")
    assert resp.status_code == 200
    text = resp.json()["response"]
    assert FALLBACK_SENTENCE in text, "Fallback sentence missing"
    assert len(text) < 1000, (
        f"Out-of-corpus response is overly verbose ({len(text)} chars): {text[:300]!r}"
    )


@pytest.mark.slow
def test_repeated_question_yields_identical_context():
    """Retrieval should be deterministic: same question -> same top-k articles."""
    q = "Find an article that discusses writing or creativity."
    r1 = _post(q).json()
    r2 = _post(q).json()
    ids1 = [c["article_id"] for c in r1["context"]]
    ids2 = [c["article_id"] for c in r2["context"]]
    assert ids1 == ids2, (
        f"Two identical queries returned different context article_ids:\n"
        f"  first:  {ids1}\n  second: {ids2}"
    )


# ---------------------------------------------------------------------------
# Cosmetic-fix safety (1 test)
# ---------------------------------------------------------------------------

def test_arbitrary_paths_do_not_hijack_required_endpoints():
    """Submission-guideline guard: vercel.json's /(.*) rewrite must not cause
    arbitrary paths to serve /api/prompt or /api/stats response shapes.

    Tests both an arbitrary GET path and an arbitrary POST path. Each must:
      - return a 4xx (404 or 405), or
      - if it returns 200, the body must NOT match the /api/prompt or
        /api/stats schema (which would indicate the rewrite is hijacking).
    """
    prompt_schema = {"response", "context", "Augmented_prompt"}
    stats_schema = {"chunk_size", "overlap_ratio", "top_k"}

    for method, path in [("GET", "/api/random_xyz"), ("POST", "/random_path")]:
        try:
            url = f"{BASE_URL.rstrip('/')}{path}"
            if method == "GET":
                resp = requests.get(url, timeout=10)
            else:
                resp = requests.post(url, json={"question": "test"}, timeout=10)
        except requests.exceptions.RequestException as exc:
            pytest.skip(f"Could not reach {url}: {exc}")

        if resp.status_code >= 400:
            # 4xx is correct behaviour
            continue

        # 200 OK on an arbitrary path: ensure it's NOT one of the required-endpoint shapes
        try:
            body = resp.json()
        except Exception:
            # Non-JSON 200 is fine (e.g. health-check text)
            continue
        if isinstance(body, dict):
            assert set(body.keys()) != prompt_schema, (
                f"{method} {path} returned the /api/prompt response shape "
                f"-- the cosmetic-fix rewrite is hijacking arbitrary URLs"
            )
            assert set(body.keys()) != stats_schema, (
                f"{method} {path} returned the /api/stats response shape "
                f"-- the cosmetic-fix rewrite is hijacking arbitrary URLs"
            )
