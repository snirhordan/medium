# Q1 precise fact

**Question:** Find an article that reframes marketing as a conversation with readers, aimed at writers who find self-promotion uncomfortable. Provide the title and author.

**top_k:** 8  |  **embedding:** `4UHRUIN-text-embedding-3-small`  |  **chat:** `4UHRUIN-gpt-5-mini`

## Config A - A (chunk=512, overlap=0.15)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.6291 | 37 | A Marketing Guide for Introverts |
| 2 | 0.5350 | 25 | Your Brand is What People Expect From You |
| 3 | 0.5322 | 111 | How to Silence the Haters in Your Head as You Write |

### gpt-5-mini response

```
Title: A Marketing Guide for Introverts
Author: Shaunta Grimes

This article reframes marketing as “just a conversation between you and your readers” (chunk [1]) and is explicitly aimed at writers who are introverts, noting “Writing is such solitary, interior work that it tends to attract introverts” (chunk [2]).
```

**Tokens:** {'completion_tokens': 656, 'prompt_tokens': 2240, 'total_tokens': 2896, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 576, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 11, 'engine_ttft_ms': 87, 'engine_ttlt_ms': 7374, 'pre_inference_ms': 262, 'service_tbt_ms': 11, 'service_ttft_ms': 795, 'service_ttlt_ms': 8020, 'total_duration_ms': 7774, 'user_visible_ttft_ms': 534}}

## Config B - B (chunk=1024, overlap=0.20)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.6336 | 37 | A Marketing Guide for Introverts |
| 2 | 0.5380 | 22 | Don’t Be a Writer, Be an Entrepreneur Who Writes |
| 3 | 0.5283 | 25 | Your Brand is What People Expect From You |
| 4 | 0.5149 | 111 | How to Silence the Haters in Your Head as You Write |

### gpt-5-mini response

```
"A Marketing Guide for Introverts" — Shaunta Grimes.

This article is aimed at introverted writers and reframes marketing as a gentle, reader-focused activity: it tells you to "think for a minute about how someone who has written a book like yours could reach you" and argues "marketing...is more like a Post-it note" rather than a sledgehammer (chunks [1], [2]).
```

**Tokens:** {'completion_tokens': 605, 'prompt_tokens': 2243, 'total_tokens': 2848, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 512, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 12, 'engine_ttft_ms': 73, 'engine_ttlt_ms': 8365, 'pre_inference_ms': 190, 'service_tbt_ms': 12, 'service_ttft_ms': 672, 'service_ttlt_ms': 8943, 'total_duration_ms': 8759, 'user_visible_ttft_ms': 481}}
