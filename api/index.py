"""
FastAPI app for the Medium-article RAG assistant.

Endpoints:
    GET  /api/stats   -- returns the RAG hyperparameter configuration.
    POST /api/prompt  -- runs the four-step RAG pipeline:
                         embed question -> retrieve top-k chunks from Pinecone
                         -> build augmented prompt -> call gpt-5-mini.

Only the assignment-permitted models are used:
    embedding: 4UHRUIN-text-embedding-3-small (1536 dim)
    chat:      4UHRUIN-gpt-5-mini

On Vercel, environment variables are injected at runtime. Locally, .env is
loaded via python-dotenv.
"""

import os
import traceback
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

# ---- hyperparameters (must match /api/stats response exactly) ----
CHUNK_SIZE = 512
OVERLAP_RATIO = 0.15
TOP_K = 8
NAMESPACE = "cfg-a"

# ---- required system prompt (assignment-fixed, do not modify the constraint text) ----
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

app = FastAPI(title="Medium RAG Assistant")

# ---- lazy-init singletons (saves cold start for /api/stats) ----
_vectorstore: Optional[PineconeVectorStore] = None
_chat: Optional[ChatOpenAI] = None


def _vectorstore_singleton() -> PineconeVectorStore:
    global _vectorstore
    if _vectorstore is None:
        embeddings = OpenAIEmbeddings(
            model=os.environ["EMBEDDING_MODEL"],
            api_key=os.environ["COURSE_OPENAI_API_KEY"],
            base_url=os.environ["COURSE_OPENAI_BASE_URL"],
            dimensions=1536,
        )
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        _vectorstore = PineconeVectorStore(
            index=pc.Index(os.environ["PINECONE_INDEX_NAME"]),
            embedding=embeddings,
            text_key="chunk",
            namespace=NAMESPACE,
        )
    return _vectorstore


def _chat_singleton() -> ChatOpenAI:
    global _chat
    if _chat is None:
        _chat = ChatOpenAI(
            model=os.environ["CHAT_MODEL"],
            api_key=os.environ["COURSE_OPENAI_API_KEY"],
            base_url=os.environ["COURSE_OPENAI_BASE_URL"],
        )
    return _chat


def build_user_prompt(question: str, hits: list) -> str:
    """Render the augmented user prompt from retrieved (Document, score) pairs."""
    lines = ["CONTEXT (retrieved Medium article chunks):\n"]
    for i, (doc, score) in enumerate(hits, 1):
        meta = doc.metadata or {}
        lines.append(
            f"[{i}] Title: \"{meta.get('title', '')}\"\n"
            f"    Author: {meta.get('author', '')}\n"
            f"    Article ID: {meta.get('article_id', '')}\n"
            f"    URL: {meta.get('url', '')}\n"
            f"    Score: {score:.4f}\n"
            f"    Chunk: {doc.page_content}\n"
        )
    lines.append(
        f"\nQUESTION:\n{question}\n\n"
        f"Answer using ONLY the context above. If the answer cannot be determined "
        f"from the context, respond exactly: "
        f"\"I don't know based on the provided Medium articles data.\""
    )
    return "\n".join(lines)


# ---- endpoints --------------------------------------------------------------

@app.get("/api/stats")
def stats():
    return {
        "chunk_size": CHUNK_SIZE,
        "overlap_ratio": OVERLAP_RATIO,
        "top_k": TOP_K,
    }


class PromptRequest(BaseModel):
    question: str


@app.get("/api/diag")
def diag():
    """Diagnostic: which env vars are visible to the function (booleans only — no values)."""
    required = [
        "EMBEDDING_MODEL", "CHAT_MODEL",
        "COURSE_OPENAI_API_KEY", "COURSE_OPENAI_BASE_URL",
        "PINECONE_API_KEY", "PINECONE_INDEX_NAME",
    ]
    import sys
    return {
        "env_present": {k: (k in os.environ and bool(os.environ[k])) for k in required},
        "python_version": sys.version,
        "vectorstore_initialised": _vectorstore is not None,
        "chat_initialised": _chat is not None,
    }


@app.post("/api/prompt")
def prompt(req: PromptRequest):
    try:
        return _prompt_impl(req)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc().splitlines()[-12:],
            },
        )


def _prompt_impl(req: PromptRequest):
    vs = _vectorstore_singleton()
    hits = vs.similarity_search_with_score(req.question, k=TOP_K)

    context = [
        {
            "article_id": str((doc.metadata or {}).get("article_id", "")),
            "title": str((doc.metadata or {}).get("title", "")),
            "chunk": doc.page_content,
            "score": float(score),
        }
        for doc, score in hits
    ]

    user_prompt = build_user_prompt(req.question, hits)

    chat = _chat_singleton()
    response = chat.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ])
    response_text = response.content if hasattr(response, "content") else str(response)

    return {
        "response": response_text,
        "context": context,
        "Augmented_prompt": {
            "System": SYSTEM_PROMPT,
            "User": user_prompt,
        },
    }


# Optional: health-check at root (useful for Vercel sanity-pings; not required).
@app.get("/")
def root():
    return {"status": "ok", "service": "medium-rag-assistant"}
