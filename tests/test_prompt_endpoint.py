"""Tests for POST /api/prompt endpoint against the RAG assignment specification."""
# To skip slow LLM-calling tests: pytest -m "not slow"
import os
import re

import pytest
import requests

BASE_URL = os.environ.get("RAG_BASE_URL", "http://localhost:3000")
PROMPT_URL = f"{BASE_URL.rstrip('/')}/api/prompt"

TOP_LEVEL_KEYS = {"response", "context", "Augmented_prompt"}
CONTEXT_ITEM_KEYS = {"article_id", "title", "chunk", "score"}
AUGMENTED_PROMPT_KEYS = {"System", "User"}

FALLBACK_SENTENCE = "I don't know based on the provided Medium articles data."

REQUIRED_SYSTEM_PROMPT = (
    "You are a Medium-article assistant that answers questions strictly and only "
    "based on the Medium articles dataset context provided to you (metadata and "
    "article passages). You must not use any external knowledge, the open internet, "
    "or information that is not explicitly contained in the retrieved context. If "
    "the answer cannot be determined from the provided context, respond: \"I don't "
    "know based on the provided Medium articles data.\" Always explain your answer "
    "using the given context, quoting or paraphrasing the relevant article passage "
    "or metadata when helpful."
)

PROBE_QUESTION = "Find an article that discusses writing or creativity."

ASSIGNMENT_EXAMPLES = [
    "Find an article that reframes marketing as a conversation with readers, aimed at writers who find self-promotion uncomfortable. Provide the title and author.",
    "List exactly 3 articles about education. Return only the titles.",
    "Find an article that argues past pandemics (such as the bubonic plague) can spur innovation and recovery, and summarise its central argument.",
    "I want practical, beginner-friendly advice on building habits that actually stick. Which article would you recommend, and why?",
]


def _normalise_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _post_prompt(question: str, timeout: int = 120):
    try:
        return requests.post(PROMPT_URL, json={"question": question}, timeout=timeout)
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Could not reach {PROMPT_URL}: {exc}")


@pytest.fixture(scope="session")
def prompt_response():
    """Session-scoped fixture: POST one benign in-corpus probe and reuse across schema tests."""
    return _post_prompt(PROBE_QUESTION)


def test_prompt_returns_200_and_json(prompt_response):
    """Spec: endpoint must respond 200 with application/json body."""
    assert prompt_response.status_code == 200, (
        f"Expected 200, got {prompt_response.status_code}: {prompt_response.text!r}"
    )
    content_type = prompt_response.headers.get("content-type", "")
    assert "application/json" in content_type.lower(), (
        f"Expected application/json content-type, got {content_type!r}"
    )


def test_response_has_top_level_keys(prompt_response):
    """Spec: output JSON has exactly three top-level keys with the assignment's exact casing."""
    body = prompt_response.json()
    assert isinstance(body, dict), f"Expected JSON object, got {type(body).__name__}"
    assert set(body.keys()) == TOP_LEVEL_KEYS, (
        f"Expected exactly {TOP_LEVEL_KEYS}, got {set(body.keys())}"
    )


def test_response_field_is_nonempty_string(prompt_response):
    """Spec: 'response' is the final natural language answer string, must be non-empty."""
    body = prompt_response.json()
    response_field = body["response"]
    assert isinstance(response_field, str), (
        f"'response' must be str, got {type(response_field).__name__}"
    )
    assert response_field.strip(), "'response' must be a non-empty string"


def test_context_is_list_of_chunk_objects(prompt_response):
    """Spec: 'context' is an array of retrieved chunk objects; each item has exactly four keys."""
    body = prompt_response.json()
    context = body["context"]
    assert isinstance(context, list), f"'context' must be a list, got {type(context).__name__}"
    assert len(context) >= 1, "'context' must contain at least one retrieved chunk"
    for i, item in enumerate(context):
        assert isinstance(item, dict), (
            f"context[{i}] must be a dict, got {type(item).__name__}"
        )
        assert set(item.keys()) == CONTEXT_ITEM_KEYS, (
            f"context[{i}] expected keys {CONTEXT_ITEM_KEYS}, got {set(item.keys())}"
        )


def test_context_field_types(prompt_response):
    """Spec: per-chunk field types -- article_id/title strings, chunk non-empty string, score numeric."""
    body = prompt_response.json()
    for i, item in enumerate(body["context"]):
        article_id = item["article_id"]
        title = item["title"]
        chunk = item["chunk"]
        score = item["score"]
        assert isinstance(article_id, str), (
            f"context[{i}].article_id must be str, got {type(article_id).__name__}"
        )
        assert isinstance(title, str), (
            f"context[{i}].title must be str, got {type(title).__name__}"
        )
        assert isinstance(chunk, str) and chunk.strip(), (
            f"context[{i}].chunk must be a non-empty string"
        )
        assert isinstance(score, (int, float)) and not isinstance(score, bool), (
            f"context[{i}].score must be a number (not bool), got {type(score).__name__}"
        )


def test_augmented_prompt_structure(prompt_response):
    """Spec: Augmented_prompt is a dict with exactly the keys 'System' and 'User', both strings."""
    body = prompt_response.json()
    augmented = body["Augmented_prompt"]
    assert isinstance(augmented, dict), (
        f"'Augmented_prompt' must be a dict, got {type(augmented).__name__}"
    )
    assert set(augmented.keys()) == AUGMENTED_PROMPT_KEYS, (
        f"Expected exactly {AUGMENTED_PROMPT_KEYS}, got {set(augmented.keys())}"
    )
    assert isinstance(augmented["System"], str), "Augmented_prompt.System must be a string"
    assert isinstance(augmented["User"], str), "Augmented_prompt.User must be a string"


def test_system_prompt_contains_required_text(prompt_response):
    """Spec safety net: System prompt must verbatim contain the assignment-mandated text."""
    body = prompt_response.json()
    actual_system = _normalise_ws(body["Augmented_prompt"]["System"])
    expected = _normalise_ws(REQUIRED_SYSTEM_PROMPT)
    assert expected in actual_system, (
        "Augmented_prompt.System does not contain the required system prompt verbatim.\n"
        f"Expected substring (whitespace-normalised):\n{expected}\n\n"
        f"Got (whitespace-normalised):\n{actual_system}"
    )


def test_system_prompt_mentions_fallback_string(prompt_response):
    """Spec: the exact fallback sentence must appear verbatim in the System prompt."""
    body = prompt_response.json()
    system_prompt = body["Augmented_prompt"]["System"]
    assert FALLBACK_SENTENCE in system_prompt, (
        f"System prompt missing required fallback sentence: {FALLBACK_SENTENCE!r}"
    )


@pytest.mark.slow
def test_out_of_corpus_question_returns_fallback():
    """Spec: out-of-corpus questions must trigger the mandated fallback response string."""
    resp = _post_prompt("What is the capital of France?")
    assert resp.status_code == 200, (
        f"Expected 200, got {resp.status_code}: {resp.text!r}"
    )
    body = resp.json()
    response_field = body.get("response", "")
    assert FALLBACK_SENTENCE in response_field, (
        f"Out-of-corpus question should yield fallback. Got: {response_field!r}"
    )


@pytest.mark.slow
@pytest.mark.parametrize("question", ASSIGNMENT_EXAMPLES)
def test_assignment_example_questions_return_nonempty(question):
    """Spec: each assignment example question must produce a non-empty response and context."""
    resp = _post_prompt(question)
    assert resp.status_code == 200, (
        f"Expected 200 for {question!r}, got {resp.status_code}: {resp.text!r}"
    )
    body = resp.json()
    response_field = body.get("response", "")
    context = body.get("context", [])
    assert isinstance(response_field, str) and response_field.strip(), (
        f"Empty 'response' for question: {question!r}"
    )
    assert isinstance(context, list) and len(context) >= 1, (
        f"Empty 'context' for question: {question!r}"
    )
