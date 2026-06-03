# Hyperparameter configuration rationale

> **Status:** preliminary recommendation pending user verification.
> All four configs were evaluated on the same 200-article subset
> (rows 0-199 of `medium-english-50mb.csv`) against the four
> assignment example questions, using only the allowed models
> `4UHRUIN-text-embedding-3-small` and `4UHRUIN-gpt-5-mini`.

## The four configs

| Config | chunk_size | overlap_ratio | Namespace | Chunks (200 articles) | Theme |
|---|---|---|---|---|---|
| **A** | 512  | 0.15 | `cfg-a` | 629  | balanced |
| **B** | 1024 | 0.20 | `cfg-b` | 353  | recall-tilt (larger chunks, more overlap) |
| **C** | 256  | 0.10 | `cfg-c` | 1135 | precision-tilt (finest chunks, lowest overlap) |
| **D** | 1024 | 0.30 | `cfg-d` | 364  | max-overlap (largest chunks, max-allowed overlap) |

All four configs were used with `top_k=8` at query time.

## Theoretical context-token cost per query (top_k=8)

Following the assignment's principle that *"pushing unnecessary data into
the model context will be considered inefficient"*, raw context size
matters:

| Config | Chunk tokens | Total context tokens / query | Relative to A |
|---|---|---|---|
| **C** | 256  | ~2,048 | 0.5x |
| **A** | 512  | ~4,096 | 1.0x |
| **B** | 1024 | ~8,192 | 2.0x |
| **D** | 1024 | ~8,192 | 2.0x |

C is theoretically the cheapest, A is the balance point, and B and D
double the context bill. This is the cost axis we want to minimise
subject to retrieval quality being adequate.

## Per-question results

### Q1 — precise fact ("marketing for introverts")

| | Top-1 article | Top-1 score | Result |
|---|---|---|---|
| A | A Marketing Guide for Introverts | 0.6291 | ✓ correct title + author, quotes the central reframe ("marketing is just a conversation between you and your readers") |
| B | A Marketing Guide for Introverts | 0.6331 | ✓ correct, quotes secondary metaphor ("Post-it note, not sledgehammer") |
| C | A Marketing Guide for Introverts | 0.6017 | ✓ correct, quotes the central reframe |
| D | A Marketing Guide for Introverts | 0.6336 | ✓ correct, broader textual support |

**All four configs answered Q1 correctly.** Marginal differences in
quote quality (A and C quote the central reframe most cleanly).

### Q2 — multi-result topic ("3 articles about education")

All four configs returned the mandated fallback **"I don't know based
on the provided Medium articles data."** This is the *correct* answer
on this subset, because rows 0-199 of the corpus do not contain
education articles (they are heavily writing/marketing-focused). This
is a **corpus-coverage issue, not a config issue**, and will be
re-evaluated on the full 7,600-article corpus.

Observation on style:
- A and C gave the **minimal fallback only**, matching the system
  prompt's explicit instruction.
- B and D appended verbose explanations enumerating the retrieved
  titles. This is technically still compliant but spends more output
  tokens.

### Q3 — key idea summary ("Manchurian Plague")

| | Top-1 article | Top-1 score | Result |
|---|---|---|---|
| A | The Manchurian Plague | 0.4620 | ✓ **Richest summary** — names Dr. Wu Lien-teh, quotes "main approach…emphasis on the wearing of cloth face masks", mentions "harsh quarantines and travel restrictions", uses article's verb "contained" |
| B | The Manchurian Plague | 0.4661 | ✓ Decent summary; mentions PPE standard, ties to COVID; no Dr. Wu Lien-teh |
| **C** | The Manchurian Plague | 0.4621 | **✗ FAILED** — chat model responded "I don't know based on the provided Medium articles data." despite the right article being retrieved |
| D | The Manchurian Plague | 0.4663 | ✓ Similar to B; "history only further underlines the need for masks…" |

**The headline finding: Config C failed Q3.** The retriever returned the
correct article (top-1, score 0.4621 — essentially identical to A and
B), but the chat model could not answer. Why? **256-token chunks were
too short to contain the central "pandemic spurs innovation" argument**.
The retrieved chunks held supporting text but missed the framing
sentence. When the LLM cannot find the argument in the context, the
system prompt forces it to fall back to "I don't know" — exactly as it
should.

This is the strongest negative against Config C, and it directly
contradicts the naive "smaller chunks are always better" hypothesis.
For Q3-style summary questions, chunks must be **long enough to hold
the article's thesis sentence**, otherwise the retrieval signal lands
on the right article but the LLM gets only fragments.

### Q4 — recommendation ("habits that stick")

All four configs retrieved the same top-2 articles (in different
orders): "How Writing 1000 Words a Day Changed my Life" (id 74) and
"The Ted Talk That Changed My Life" (id 14).

| | Recommended article | Tactic cited |
|---|---|---|
| A | The Ted Talk That Changed My Life | 3-pillar habit framework (trigger → behavior → reward), mindfulness pause |
| B | How Writing 1000 Words a Day | Environment design, consistency, "always carry a notebook" |
| C | How Writing 1000 Words a Day | Environment design, identity-based habits, write-night-before hack |
| D | The Ted Talk That Changed My Life | 3-pillar habit framework, mindfulness pause |

The recommended article differs (A and D pick the habit-pillar article;
B and C pick the writing-habit article). The question asks about habits
*in general*, not writing habits specifically — so the habit-pillar
article ("Ted Talk") is the more on-topic recommendation. A and D align
with the question intent more directly.

### Q1-Q4 summary

| | Q1 | Q2 | Q3 | Q4 | Context tokens / query |
|---|---|---|---|---|---|
| **A** | ✓ rich quote | ✓ minimal fallback | ✓ **richest summary** | ✓ habit-pillar article | **~4,096** |
| B | ✓ ok quote | ✓ verbose fallback | ✓ decent summary | ✗ writing-specific recommendation | ~8,192 |
| **C** | ✓ rich quote | ✓ minimal fallback | **✗ FAILED** | ✗ writing-specific recommendation | ~2,048 |
| D | ✓ ok quote | ✓ verbose fallback | ✓ decent summary | ✓ habit-pillar article | ~8,192 |

## Why A wins (proposed; user to verify)

**A is the only config that succeeds on all four questions AND uses
moderate context.**

1. **C is disqualified** by the Q3 failure. The cost savings from
   2,048-token contexts mean nothing if the system cannot answer
   summary-style questions. C is on the wrong side of the
   "chunks too small to hold thesis" cliff.

2. **B and D are penalised** by the *efficiency principle*: both
   consume ~8,192 context tokens per query (2x A, 4x C). On Q1 and
   Q3 they retrieve essentially the same articles A does, at the same
   top scores — the doubled context is not buying retrieval quality.
   D in particular adds 30% overlap on top of 1024-token chunks, which
   is the maximum-redundancy point in the design space; it should be
   the worst on the efficiency axis if it doesn't beat A on quality,
   and it doesn't.

3. **A's Q3 quality dominates.** A's summary is the only one that
   names Dr. Wu Lien-teh and quotes the article's own description of
   his clinical innovations — exactly the "central argument" the
   question asks for. B's and D's summaries are decent but more
   abstract.

4. **A picks the right article for Q4.** Both A and D get the
   habit-pillar article; B and C drift to the writing-habit article.
   Combined with the Q3 advantage, A is the most consistent across
   the four question types.

5. **A's context tokens are 4,096 — half of B/D.** Following the
   assignment's stated grading criterion that "pushing unnecessary
   data into the model context will be considered inefficient", A is
   the better choice than B or D when retrieval quality is comparable.

## Open question (for full-corpus evaluation)

Q2 cannot be discriminated on this subset because rows 0-199 do not
contain any education articles. Once the full 7,600-article corpus is
embedded into the winning config's namespace, Q2 retrieval (especially
the "3 *distinct* articles" requirement) becomes the strongest test of
chunk granularity. If A handles Q2 correctly at full scale, the
recommendation is settled. If A struggles to dedup to 3 distinct
articles, a re-evaluation with `top_k=12-15` may be warranted (top-k
is a query-time knob — no re-embedding required).

## Recommendation

Use Config A:
- `chunk_size = 512`
- `overlap_ratio = 0.15`
- `top_k = 8` (revisit at query time after full-corpus embedding)
- Pinecone namespace: `cfg-a` (will become the deployed namespace)

`/api/stats` will report:
```json
{"chunk_size": 512, "overlap_ratio": 0.15, "top_k": 8}
```

## Next steps (pending user verification)

1. **User verifies the choice of A.** Open `eval_results/q1..q4_*.md` to
   inspect any of the four runs end-to-end.
2. On approval: delete the three losing namespaces (`cfg-b`, `cfg-c`,
   `cfg-d`) from Pinecone in a single API call each.
3. Embed the remaining ~7,482 articles (rows 200-7681) into `cfg-a`
   with the same chunk_size/overlap (`OFFSET=200 CONFIG=A python
   chunk_and_embed.py`). Expected cost: ~$0.30, ~30 min.
4. Re-run Q2 at full scale to confirm dedup-to-3 works on real
   education articles.
5. Build the `/api/prompt` and `/api/stats` endpoints; deploy to
   Vercel; run the pytest suite against the deployed URL.

## Cumulative cost so far

- Embeddings (4 configs × 200 articles): ~1.3M tokens at $0.02/1M
  ≈ **$0.026**
- Chat evaluation (16 LLM calls): prompt 35,186 + completion 12,174
  ≈ **$0.025**
- **Total ≈ $0.05 of $5 budget**.
