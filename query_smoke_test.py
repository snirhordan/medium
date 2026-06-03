"""
Side-by-side RAG evaluation of configs A and B.

For each of the four assignment example questions, retrieve top-k chunks from
each namespace (cfg-a and cfg-b), build the augmented prompt, call the chat
model, and print the answers side by side so you can pick a winner.

Allowed models only:
    embedding:  4UHRUIN-text-embedding-3-small  (1536 dim)
    chat:       4UHRUIN-gpt-5-mini

Usage:
    # prerequisite: ran chunk_and_embed.py twice (CONFIG=A and CONFIG=B)
    python query_smoke_test.py

    # tweak top_k without re-embedding:
    TOP_K=10 python query_smoke_test.py
"""

import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# ---- assignment-fixed values ----------------------------------------------
SYSTEM_PROMPT = (
    "You are a Medium-article assistant that answers questions strictly and only "
    "based on the Medium articles dataset context provided to you (metadata and "
    "article passages). You must not use any external knowledge, the open internet, "
    "or information that is not explicitly contained in the retrieved context. "
    "If the answer cannot be determined from the provided context, respond: "
    "\"I don't know based on the provided Medium articles data.\" "
    "Always explain your answer using the given context, quoting or paraphrasing "
    "the relevant article passage or metadata when helpful.\n\n"
    "Style: keep responses concise. For list questions, return only the requested "
    "fields. For summary questions, 3-5 sentences. For recommendation questions, "
    "name the article first, then justify in 2-3 sentences."
)

ASSIGNMENT_EXAMPLES = [
    ("Q1 precise fact",
     "Find an article that reframes marketing as a conversation with readers, "
     "aimed at writers who find self-promotion uncomfortable. Provide the title "
     "and author."),
    ("Q2 multi-result topic",
     "List exactly 3 articles about education. Return only the titles."),
    ("Q3 key idea summary",
     "Find an article that argues past pandemics (such as the bubonic plague) can "
     "spur innovation and recovery, and summarise its central argument."),
    ("Q4 recommendation",
     "I want practical, beginner-friendly advice on building habits that actually "
     "stick. Which article would you recommend, and why?"),
]

CONFIGS = {
    "A": {"namespace": "cfg-a", "label": "A (chunk=512, overlap=0.15)"},
    "B": {"namespace": "cfg-b", "label": "B (chunk=1024, overlap=0.20)"},
    "C": {"namespace": "cfg-c", "label": "C (chunk=256, overlap=0.10)"},
    "D": {"namespace": "cfg-d", "label": "D (chunk=1024, overlap=0.30)"},
}
CONFIG_ORDER = ("A", "B", "C", "D")

TOP_K = int(os.environ.get("TOP_K", "8"))
USAGE_LOG = Path("logs/eval_usage.jsonl")
EVAL_DIR = Path("eval_results")
# ---------------------------------------------------------------------------

load_dotenv()

embeddings = OpenAIEmbeddings(
    model=os.environ["EMBEDDING_MODEL"],
    api_key=os.environ["COURSE_OPENAI_API_KEY"],
    base_url=os.environ["COURSE_OPENAI_BASE_URL"],
    dimensions=1536,
)
chat = ChatOpenAI(
    model=os.environ["CHAT_MODEL"],
    api_key=os.environ["COURSE_OPENAI_API_KEY"],
    base_url=os.environ["COURSE_OPENAI_BASE_URL"],
)
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
INDEX = pc.Index(os.environ["PINECONE_INDEX_NAME"])

USAGE_LOG.parent.mkdir(exist_ok=True)


def vectorstore_for(namespace: str) -> PineconeVectorStore:
    return PineconeVectorStore(
        index=INDEX,
        embedding=embeddings,
        text_key="chunk",
        namespace=namespace,
    )


def build_user_prompt(question: str, hits: list[tuple]) -> str:
    """Render the augmented user prompt from retrieved (doc, score) pairs."""
    lines = ["CONTEXT (retrieved Medium article chunks):\n"]
    for i, (doc, score) in enumerate(hits, 1):
        meta = doc.metadata
        lines.append(
            f"[{i}] Title: \"{meta.get('title', '')}\"\n"
            f"    Author: {meta.get('author', '')}\n"
            f"    Article ID: {meta.get('article_id', '')}\n"
            f"    URL: {meta.get('url', '')}\n"
            f"    Score: {score:.4f}\n"
            f"    Chunk: {doc.page_content[:800]}\n"
        )
    lines.append(
        f"\nQUESTION:\n{question}\n\n"
        f"Answer using ONLY the context above. If the answer cannot be determined "
        f"from the context, respond exactly: "
        f"\"I don't know based on the provided Medium articles data.\""
    )
    return "\n".join(lines)


def run_one(cfg_key: str, question: str) -> dict:
    ns = CONFIGS[cfg_key]["namespace"]
    vs = vectorstore_for(ns)
    hits = vs.similarity_search_with_score(question, k=TOP_K)

    user_prompt = build_user_prompt(question, hits)
    response = chat.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ])
    text = response.content if hasattr(response, "content") else str(response)

    # log token usage if surfaced
    usage_meta = getattr(response, "response_metadata", {}) or {}
    token_usage = usage_meta.get("token_usage") or {}
    with USAGE_LOG.open("a") as f:
        f.write(json.dumps({
            "config": cfg_key,
            "question": question[:80],
            "prompt_tokens": token_usage.get("prompt_tokens"),
            "completion_tokens": token_usage.get("completion_tokens"),
            "total_tokens": token_usage.get("total_tokens"),
            "t": time.time(),
        }) + "\n")

    return {
        "config": cfg_key,
        "namespace": ns,
        "question": question,
        "hits": [
            {
                "title": h[0].metadata.get("title", ""),
                "article_id": h[0].metadata.get("article_id", ""),
                "score": h[1],
            }
            for h in hits
        ],
        "response": text,
        "token_usage": token_usage,
    }


def render_side_by_side(label: str, qa: str, results: dict, active_configs) -> None:
    print("=" * 100)
    print(f"{label}\n{qa}")
    print("=" * 100)
    for cfg_key in active_configs:
        r = results[cfg_key]
        print(f"\n[ Config {cfg_key} - {CONFIGS[cfg_key]['label']} | top_k={TOP_K} ]")
        print(f"Retrieved articles (deduped on article_id, top 5 shown):")
        seen = set()
        for h in r["hits"]:
            if h["article_id"] in seen:
                continue
            seen.add(h["article_id"])
            print(f"   score={h['score']:.4f}  id={h['article_id']:>4}  "
                  f"\"{h['title'][:80]}\"")
            if len(seen) >= 5:
                break
        print(f"\nResponse from gpt-5-mini:")
        print("   " + r["response"].replace("\n", "\n   "))
        if r["token_usage"]:
            print(f"\nTokens: {r['token_usage']}")
    print()


def write_markdown(idx: int, label: str, question: str, results: dict, active_configs) -> Path:
    """Write one markdown file per question with all evaluated configs side-by-side."""
    EVAL_DIR.mkdir(exist_ok=True)
    safe = label.replace(" ", "_").replace("/", "_").lower()
    path = EVAL_DIR / f"q{idx}_{safe}.md"
    lines = []
    lines.append(f"# {label}")
    lines.append("")
    lines.append(f"**Question:** {question}")
    lines.append("")
    lines.append(f"**top_k:** {TOP_K}  |  **embedding:** `{os.environ['EMBEDDING_MODEL']}`  |  **chat:** `{os.environ['CHAT_MODEL']}`")
    lines.append("")
    for cfg_key in active_configs:
        r = results[cfg_key]
        lines.append(f"## Config {cfg_key} - {CONFIGS[cfg_key]['label']}")
        lines.append("")
        lines.append("### Retrieved articles (deduped on article_id, top 5)")
        lines.append("")
        lines.append("| rank | score | article_id | title |")
        lines.append("|---|---|---|---|")
        seen = set()
        rank = 0
        for h in r["hits"]:
            if h["article_id"] in seen:
                continue
            seen.add(h["article_id"])
            rank += 1
            title = h["title"].replace("|", "\\|")[:120]
            lines.append(f"| {rank} | {h['score']:.4f} | {h['article_id']} | {title} |")
            if rank >= 5:
                break
        lines.append("")
        lines.append("### gpt-5-mini response")
        lines.append("")
        lines.append("```")
        lines.append(r["response"])
        lines.append("```")
        lines.append("")
        if r["token_usage"]:
            lines.append(f"**Tokens:** {r['token_usage']}")
            lines.append("")
    path.write_text("\n".join(lines))
    return path


def main() -> int:
    print(f"[eval] top_k={TOP_K} | configs={list(CONFIGS)}")
    print(f"[eval] embedding={os.environ['EMBEDDING_MODEL']}")
    print(f"[eval] chat={os.environ['CHAT_MODEL']}\n")

    # sanity: confirm each namespace actually has vectors; skip those that are empty
    active_configs = list(CONFIG_ORDER)
    try:
        stats = INDEX.describe_index_stats()
        for cfg_key in CONFIG_ORDER:
            ns = CONFIGS[cfg_key]["namespace"]
            count = stats.get("namespaces", {}).get(ns, {}).get("vector_count", 0)
            print(f"[eval] namespace {ns}: {count} vectors")
            if count == 0:
                print(f"[warn] namespace {ns} is empty - skipping config {cfg_key}.")
                active_configs.remove(cfg_key)
    except Exception as e:
        print(f"[warn] could not check stats: {e}")

    grand_total = {"prompt": 0, "completion": 0}
    written = []
    for idx, (label, question) in enumerate(ASSIGNMENT_EXAMPLES, 1):
        results = {}
        for cfg_key in active_configs:
            results[cfg_key] = run_one(cfg_key, question)
            tu = results[cfg_key]["token_usage"]
            if tu:
                grand_total["prompt"] += tu.get("prompt_tokens", 0) or 0
                grand_total["completion"] += tu.get("completion_tokens", 0) or 0
        render_side_by_side(label, question, results, active_configs)
        md_path = write_markdown(idx, label, question, results, active_configs)
        written.append(md_path)
        print(f"[eval] wrote {md_path}")

    print("=" * 100)
    print(f"[eval] cumulative chat tokens for this eval: "
          f"prompt={grand_total['prompt']:,} completion={grand_total['completion']:,}")
    print(f"[eval] usage log: {USAGE_LOG}")
    print(f"[eval] markdown side-by-side files written:")
    for p in written:
        print(f"   {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
