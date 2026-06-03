# Q4 recommendation

**Question:** I want practical, beginner-friendly advice on building habits that actually stick. Which article would you recommend, and why?

**top_k:** 8  |  **embedding:** `4UHRUIN-text-embedding-3-small`  |  **chat:** `4UHRUIN-gpt-5-mini`

## Config A - A (chunk=512, overlap=0.15)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.5567 | 74 | How Writing 1000 Words a Day Changed my Life |
| 2 | 0.5109 | 14 | The Ted Talk That Changed My Life |
| 3 | 0.4881 | 31 | The Simple Formula For Becoming A Better Writer |
| 4 | 0.4798 | 88 | ‘Am I Just Lazy?’ |
| 5 | 0.4692 | 17 | An Effective Five-Step Process for Writing Captivating Headlines |

### gpt-5-mini response

```
"The Ted Talk That Changed My Life" by David Liira.

This piece lays out a simple, beginner-friendly model — “the 3 pillars that form a habit: you experience a trigger. You respond with a behavior. You receive a reward” — and frames a practical tactic (a brief mindful pause) to interrupt automatic, stress-driven responses. It also explains why that pause works by noting the prefrontal cortex (the part that supports self-control) goes offline under stress, making the advice easy to apply and understand.
```

**Tokens:** {'completion_tokens': 692, 'prompt_tokens': 2215, 'total_tokens': 2907, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 576, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 2176}, 'latency_checkpoint': {'engine_tbt_ms': 11, 'engine_ttft_ms': 51, 'engine_ttlt_ms': 8296, 'pre_inference_ms': 165, 'service_tbt_ms': 11, 'service_ttft_ms': 615, 'service_ttlt_ms': 8860, 'total_duration_ms': 8707, 'user_visible_ttft_ms': 451}}

## Config B - B (chunk=1024, overlap=0.20)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.5864 | 74 | How Writing 1000 Words a Day Changed my Life |
| 2 | 0.5119 | 88 | ‘Am I Just Lazy?’ |
| 3 | 0.5098 | 14 | The Ted Talk That Changed My Life |
| 4 | 0.4879 | 31 | The Simple Formula For Becoming A Better Writer |
| 5 | 0.4648 | 24 | Why Writing Online Is Different |

### gpt-5-mini response

```
"How Writing 1000 Words a Day Changed my Life" by Srinivas Rao.

This piece emphasizes practical, beginner-friendly steps for making a habit stick—“By showing up every day, you tap into the profound power of consistency” —and gives concrete tactics like “Design an Environment Conducive to Writing” and to “Always Carry a Notebook.” It also shows real outcomes from those habits (it “led to a 2 book deal” and helped finish a “45,000 word manuscript”), demonstrating the advice produces lasting results.
```

**Tokens:** {'completion_tokens': 759, 'prompt_tokens': 2218, 'total_tokens': 2977, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 640, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 2176}, 'latency_checkpoint': {'engine_tbt_ms': 13, 'engine_ttft_ms': 48, 'engine_ttlt_ms': 9743, 'pre_inference_ms': 159, 'service_tbt_ms': 13, 'service_ttft_ms': 602, 'service_ttlt_ms': 10277, 'total_duration_ms': 10168, 'user_visible_ttft_ms': 443}}

## Config C - C (chunk=256, overlap=0.10)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.5792 | 74 | How Writing 1000 Words a Day Changed my Life |
| 2 | 0.5129 | 14 | The Ted Talk That Changed My Life |
| 3 | 0.4919 | 101 | 5 ways to hack your workspace |
| 4 | 0.4918 | 88 | ‘Am I Just Lazy?’ |

### gpt-5-mini response

```
How Writing 1000 Words a Day Changed my Life

This article gives concrete, beginner-friendly habit tactics: it tells you to “Design an Environment Conducive to Writing” (e.g., surround yourself with books and notebooks), treats habits as identity-based (“This is no longer something I just do. It’s who I am.”), and offers simple execution hacks—“set it up the night before,” use a distraction‑free tool, or even “write one sentence the night before”—all practical steps to make a habit stick.
```

**Tokens:** {'completion_tokens': 823, 'prompt_tokens': 2163, 'total_tokens': 2986, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 704, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 12, 'engine_ttft_ms': 67, 'engine_ttlt_ms': 9536, 'pre_inference_ms': 192, 'service_tbt_ms': 11, 'service_ttft_ms': 729, 'service_ttlt_ms': 10169, 'total_duration_ms': 9998, 'user_visible_ttft_ms': 537}}

## Config D - D (chunk=1024, overlap=0.30)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.5680 | 74 | How Writing 1000 Words a Day Changed my Life |
| 2 | 0.5284 | 88 | ‘Am I Just Lazy?’ |
| 3 | 0.5097 | 14 | The Ted Talk That Changed My Life |
| 4 | 0.4880 | 31 | The Simple Formula For Becoming A Better Writer |

### gpt-5-mini response

```
The Ted Talk That Changed My Life

This article lays out a simple, practical framework for habits — “the 3 pillars that form a habit: You experience a trigger. You respond with a behavior. You receive a reward” — and shows how a basic mindfulness practice can be used at the trigger to change behavior (noting “The Simplest Form of Mindfulness Is Also the Most Effective”). That clear, bite-sized explanation and example make it beginner-friendly for building habits that stick.
```

**Tokens:** {'completion_tokens': 620, 'prompt_tokens': 2211, 'total_tokens': 2831, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 512, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 12, 'engine_ttft_ms': 73, 'engine_ttlt_ms': 7654, 'pre_inference_ms': 134, 'service_tbt_ms': 12, 'service_ttft_ms': 581, 'service_ttlt_ms': 8157, 'total_duration_ms': 8032, 'user_visible_ttft_ms': 446}}
