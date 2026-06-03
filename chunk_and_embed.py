"""
Chunk Medium articles, embed via LLMod.ai (OpenAI-compatible) using LangChain,
and upsert into Pinecone.

Two configs share the same Pinecone index via separate namespaces:
    CONFIG=A   chunk_size=512   overlap=0.15   namespace=cfg-a    (balanced)
    CONFIG=B   chunk_size=1024  overlap=0.20   namespace=cfg-b    (recall-tilted)

Only the allowed models are referenced:
    embedding: 4UHRUIN-text-embedding-3-small (1536 dim)

Run order:
    # smoke test, config A, 200 articles (~$0.01)
    CONFIG=A LIMIT=200 python chunk_and_embed.py

    # smoke test, config B, 200 articles (~$0.01)
    CONFIG=B LIMIT=200 python chunk_and_embed.py

    # then evaluate (query_smoke_test.py), pick the winner, scale up:
    CONFIG=<winner> python chunk_and_embed.py     # full 7600 articles

Re-runs are idempotent: vector IDs are deterministic ({article_id}-{chunk_idx}),
so upserts overwrite cleanly within a namespace.
"""

import json
import os
import sys
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import TokenTextSplitter
from pinecone import Pinecone

# ---- two configs, keyed by the CONFIG env var -----------------------------
CONFIGS = {
    "A": {"chunk_size": 512,  "overlap_ratio": 0.15, "namespace": "cfg-a"},
    "B": {"chunk_size": 1024, "overlap_ratio": 0.20, "namespace": "cfg-b"},
}
EMBED_BATCH = 96
UPSERT_BATCH = 100
CSV_PATH = "medium-english-50mb.csv"
# ---------------------------------------------------------------------------

load_dotenv()

CONFIG_KEY = os.environ.get("CONFIG", "A").upper()
if CONFIG_KEY not in CONFIGS:
    sys.exit(f"CONFIG must be one of {list(CONFIGS)}, got {CONFIG_KEY!r}")
cfg = CONFIGS[CONFIG_KEY]
CHUNK_SIZE = cfg["chunk_size"]
OVERLAP_RATIO = cfg["overlap_ratio"]
CHUNK_OVERLAP = int(CHUNK_SIZE * OVERLAP_RATIO)
NAMESPACE = cfg["namespace"]

EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]   # locked: 4UHRUIN-text-embedding-3-small
INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]
LIMIT = int(os.environ.get("LIMIT", "0")) or None
OFFSET = int(os.environ.get("OFFSET", "0"))

USAGE_LOG = Path(f"logs/usage_{CONFIG_KEY.lower()}.jsonl")
USAGE_LOG.parent.mkdir(exist_ok=True)

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=os.environ["COURSE_OPENAI_API_KEY"],
    base_url=os.environ["COURSE_OPENAI_BASE_URL"],
    dimensions=1536,
    chunk_size=EMBED_BATCH,   # LangChain's name for the embedding *batch* size
)
splitter = TokenTextSplitter(
    encoding_name="cl100k_base",
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
vectorstore = PineconeVectorStore(
    index=pc.Index(INDEX_NAME),
    embedding=embeddings,
    text_key="chunk",          # page_content lands in metadata["chunk"]
    namespace=NAMESPACE,
)


def log_usage(n_docs: int, total_chars: int) -> None:
    with USAGE_LOG.open("a") as f:
        f.write(json.dumps({
            "config": CONFIG_KEY,
            "n_docs": n_docs,
            "approx_tokens": total_chars // 4,
            "t": time.time(),
        }) + "\n")


def safe_str(v) -> str:
    if v is None:
        return ""
    s = str(v)
    return "" if s == "nan" else s


def main() -> int:
    print(f"[config {CONFIG_KEY}] chunk_size={CHUNK_SIZE} overlap={CHUNK_OVERLAP} "
          f"(ratio={OVERLAP_RATIO}) namespace={NAMESPACE}")
    print(f"[config {CONFIG_KEY}] limit={LIMIT or 'full'} offset={OFFSET}")
    print(f"[config {CONFIG_KEY}] index={INDEX_NAME} model={EMBEDDING_MODEL}")

    df = pd.read_csv(CSV_PATH)
    n_total = len(df)
    end = min(n_total, OFFSET + LIMIT) if LIMIT else n_total
    print(f"[csv] {n_total} rows; processing [{OFFSET}, {end})")

    pending_ids: list[str] = []
    pending_docs: list[Document] = []
    article_count = 0
    chunk_count = 0
    t0 = time.time()
    last_print = t0

    def flush(force: bool = False) -> None:
        nonlocal pending_ids, pending_docs
        while (force and pending_docs) or len(pending_docs) >= UPSERT_BATCH:
            n = min(UPSERT_BATCH, len(pending_docs))
            batch_ids = pending_ids[:n]
            batch_docs = pending_docs[:n]
            pending_ids = pending_ids[n:]
            pending_docs = pending_docs[n:]
            vectorstore.add_documents(documents=batch_docs, ids=batch_ids)
            log_usage(n_docs=n, total_chars=sum(len(d.page_content) for d in batch_docs))

    for row_idx in range(OFFSET, end):
        row = df.iloc[row_idx]
        body = safe_str(row.get("text"))
        if not body.strip():
            continue
        title = safe_str(row.get("title"))
        article_id = str(row_idx)
        full_text = f"{title}\n\n{body}" if title else body
        chunks = splitter.split_text(full_text)

        for k, chunk in enumerate(chunks):
            pending_ids.append(f"{article_id}-{k}")
            pending_docs.append(Document(
                page_content=chunk,
                metadata={
                    "article_id": article_id,
                    "title": title[:512],
                    "author": safe_str(row.get("authors"))[:256],
                    "url": safe_str(row.get("url"))[:512],
                    "tags": safe_str(row.get("tags"))[:256],
                    "chunk_idx": k,
                },
            ))

        article_count += 1
        chunk_count += len(chunks)
        flush(force=False)

        if time.time() - last_print > 5:
            elapsed = time.time() - t0
            rate = article_count / elapsed if elapsed > 0 else 0
            print(f"[progress {CONFIG_KEY}] {article_count} articles, {chunk_count} chunks, "
                  f"{elapsed:.0f}s elapsed, {rate:.1f} art/s, pending={len(pending_docs)}")
            last_print = time.time()

    flush(force=True)

    elapsed = time.time() - t0
    print(f"[done {CONFIG_KEY}] {article_count} articles -> {chunk_count} chunks "
          f"in {elapsed:.0f}s")

    if USAGE_LOG.exists():
        total = sum(
            json.loads(l).get("approx_tokens", 0)
            for l in USAGE_LOG.read_text().splitlines() if l.strip()
        )
        print(f"[tokens {CONFIG_KEY}] approx embedding tokens (char/4 estimate): {total:,}")

    try:
        stats = pc.Index(INDEX_NAME).describe_index_stats()
        ns_stats = stats.get("namespaces", {}).get(NAMESPACE, {})
        print(f"[pinecone] namespace {NAMESPACE} now has "
              f"{ns_stats.get('vector_count', '?')} vectors")
    except Exception as e:
        print(f"[pinecone] could not fetch stats: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
