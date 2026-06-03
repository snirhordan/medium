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
The Ted Talk That Changed My Life

This article explains the habit mechanics in a beginner-friendly way — it lays out the “3 pillars that form a habit: you experience a trigger, you respond with a behavior, you receive a reward” and shows a simple practical tactic: “taking a split second” (a mindfulness pause) to interrupt automatic responses. It also highlights why this matters by noting your prefrontal cortex (the part that governs that pause) “is the first to go offline when we get stressed,” so the piece gives a clear, practical strategy to make better habit choices.
```

**Tokens:** {'completion_tokens': 577, 'prompt_tokens': 2215, 'total_tokens': 2792, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 448, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 12, 'engine_ttft_ms': 73, 'engine_ttlt_ms': 7102, 'pre_inference_ms': 138, 'service_tbt_ms': 12, 'service_ttft_ms': 1092, 'service_ttlt_ms': 8119, 'total_duration_ms': 7996, 'user_visible_ttft_ms': 954}}

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
"The Ted Talk That Changed My Life"

This article explains habit formation as three clear pillars — “You experience a trigger. You respond with a behavior. You receive a reward.” — and recommends the practical, beginner-friendly technique of using a moment of mindfulness to interrupt the automatic response, noting that under stress “our prefrontal cortex ... is the first to go offline” so a split-second pause can prevent falling back into bad habits. These concrete concepts (identify triggers, pause, choose your behavior) make it easy to apply for someone building habits that stick.
```

**Tokens:** {'completion_tokens': 698, 'prompt_tokens': 2218, 'total_tokens': 2916, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 576, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 11, 'engine_ttft_ms': 75, 'engine_ttlt_ms': 8133, 'pre_inference_ms': 159, 'service_tbt_ms': 11, 'service_ttft_ms': 624, 'service_ttlt_ms': 8666, 'total_duration_ms': 8520, 'user_visible_ttft_ms': 464}}
