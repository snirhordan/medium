# Q2 multi-result topic

**Question:** List exactly 3 articles about education. Return only the titles.

**top_k:** 8  |  **embedding:** `4UHRUIN-text-embedding-3-small`  |  **chat:** `4UHRUIN-gpt-5-mini`

## Config A - A (chunk=512, overlap=0.15)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.3484 | 90 | Write for Towards Data Science |
| 2 | 0.3450 | 35 | Avoid Clickbait: Headline Techniques Used by Six Reputable Media Sites |
| 3 | 0.3435 | 105 | The Innovation Submission and Design Guide |
| 4 | 0.3210 | 22 | Don’t Be a Writer, Be an Entrepreneur Who Writes |
| 5 | 0.3045 | 17 | An Effective Five-Step Process for Writing Captivating Headlines |

### gpt-5-mini response

```
I don't know based on the provided Medium articles data.
```

**Tokens:** {'completion_tokens': 533, 'prompt_tokens': 2101, 'total_tokens': 2634, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 512, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 2048}, 'latency_checkpoint': {'engine_tbt_ms': 13, 'engine_ttft_ms': 40, 'engine_ttlt_ms': 7742, 'pre_inference_ms': 275, 'service_tbt_ms': 13, 'service_ttft_ms': 1201, 'service_ttlt_ms': 8891, 'total_duration_ms': 8637, 'user_visible_ttft_ms': 925}}

## Config B - B (chunk=1024, overlap=0.20)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.3559 | 35 | Avoid Clickbait: Headline Techniques Used by Six Reputable Media Sites |
| 2 | 0.3089 | 90 | Write for Towards Data Science |
| 3 | 0.3022 | 105 | The Innovation Submission and Design Guide |
| 4 | 0.2909 | 115 | Why Word Placement Is Important in Headlines |
| 5 | 0.2893 | 36 | How a Single Medium Article Received 100,000 Views |

### gpt-5-mini response

```
I don't know based on the provided Medium articles data.
```

**Tokens:** {'completion_tokens': 661, 'prompt_tokens': 2216, 'total_tokens': 2877, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 640, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 2176}, 'latency_checkpoint': {'engine_tbt_ms': 12, 'engine_ttft_ms': 38, 'engine_ttlt_ms': 8660, 'pre_inference_ms': 153, 'service_tbt_ms': 12, 'service_ttft_ms': 586, 'service_ttlt_ms': 9202, 'total_duration_ms': 9060, 'user_visible_ttft_ms': 433}}

## Config C - C (chunk=256, overlap=0.10)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.3414 | 90 | Write for Towards Data Science |
| 2 | 0.3383 | 35 | Avoid Clickbait: Headline Techniques Used by Six Reputable Media Sites |
| 3 | 0.3214 | 105 | The Innovation Submission and Design Guide |
| 4 | 0.3151 | 143 | The 5 Best Ways to Write More Articles |
| 5 | 0.3142 | 22 | Don’t Be a Writer, Be an Entrepreneur Who Writes |

### gpt-5-mini response

```
I don't know based on the provided Medium articles data.
```

**Tokens:** {'completion_tokens': 725, 'prompt_tokens': 2102, 'total_tokens': 2827, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 704, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 14, 'engine_ttft_ms': 65, 'engine_ttlt_ms': 10764, 'pre_inference_ms': 151, 'service_tbt_ms': 14, 'service_ttft_ms': 578, 'service_ttlt_ms': 11272, 'total_duration_ms': 11133, 'user_visible_ttft_ms': 427}}

## Config D - D (chunk=1024, overlap=0.30)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.3560 | 35 | Avoid Clickbait: Headline Techniques Used by Six Reputable Media Sites |
| 2 | 0.3024 | 105 | The Innovation Submission and Design Guide |
| 3 | 0.2972 | 22 | Don’t Be a Writer, Be an Entrepreneur Who Writes |
| 4 | 0.2912 | 115 | Why Word Placement Is Important in Headlines |
| 5 | 0.2895 | 36 | How a Single Medium Article Received 100,000 Views |

### gpt-5-mini response

```
I don't know based on the provided Medium articles data.

The provided titles and chunks (for example, "Avoid Clickbait: Headline Techniques Used by Six Reputable Media Sites"; "The Innovation Submission and Design Guide"; "Don’t Be a Writer, Be an Entrepreneur Who Writes"; "Why Word Placement Is Important in Headlines"; "How a Single Medium Article Received 100,000 Views"; "Write for Towards Data Science"; "Being Well Pub Launches Medika to Expand Our Writers’ Reach") cover headlines, submission guidelines, blogging, Medium traffic, and medical publishing — none are identified as being about education in the given context.
```

**Tokens:** {'completion_tokens': 842, 'prompt_tokens': 2148, 'total_tokens': 2990, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 704, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 13, 'engine_ttft_ms': 71, 'engine_ttlt_ms': 11330, 'pre_inference_ms': 275, 'service_tbt_ms': 13, 'service_ttft_ms': 756, 'service_ttlt_ms': 11986, 'total_duration_ms': 11722, 'user_visible_ttft_ms': 481}}
