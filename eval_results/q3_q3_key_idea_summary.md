# Q3 key idea summary

**Question:** Find an article that argues past pandemics (such as the bubonic plague) can spur innovation and recovery, and summarise its central argument.

**top_k:** 8  |  **embedding:** `4UHRUIN-text-embedding-3-small`  |  **chat:** `4UHRUIN-gpt-5-mini`

## Config A - A (chunk=512, overlap=0.15)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.4620 | 120 | The Manchurian Plague |
| 2 | 0.4509 | 11 | Facing Three Fundamental Coronavirus Fears |
| 3 | 0.4481 | 142 | Subject, Consumer, or Citizen: Three Post-Covid Futures |
| 4 | 0.4313 | 173 | I Hope This Pandemic Has Taught Us That Products Can’t Replace People |
| 5 | 0.4254 | 29 | How to Be Productive and Creative in Times of Panic |

### gpt-5-mini response

```
Article: "The Manchurian Plague" by Ben Kageyama.

Summary: The article argues that past pandemics can drive public‑health innovation and recovery by forcing new practices into standard use — for example, the 1910 Manchurian plague is described as “an event widely credited for making the use of personal protective equipment a standard.” It shows how Dr. Wu Lien‑teh’s “innovative” emphasis on cloth face masks and other PPE, plus harsh quarantine, isolation and travel restrictions, helped contain the disease to Manchuria and changed future disease‑control practices.
```

**Tokens:** {'completion_tokens': 902, 'prompt_tokens': 2175, 'total_tokens': 3077, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 768, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 11, 'engine_ttft_ms': 78, 'engine_ttlt_ms': 10597, 'pre_inference_ms': 137, 'service_tbt_ms': 11, 'service_ttft_ms': 580, 'service_ttlt_ms': 11115, 'total_duration_ms': 10982, 'user_visible_ttft_ms': 443}}

## Config B - B (chunk=1024, overlap=0.20)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.4661 | 120 | The Manchurian Plague |
| 2 | 0.4398 | 29 | How to Be Productive and Creative in Times of Panic |
| 3 | 0.4253 | 11 | Facing Three Fundamental Coronavirus Fears |
| 4 | 0.4150 | 142 | Subject, Consumer, or Citizen: Three Post-Covid Futures |
| 5 | 0.3999 | 70 | Only 49% of Americans Plan to Get Vaccinated Against COVID-19. Yes, You Should Be That Shocked |

### gpt-5-mini response

```
"The Manchurian Plague" — The article argues that past pandemics can drive public-health innovation by changing practices and standards. It uses the Manchurian Plague of 1910 as an example, saying this event "was an event widely credited for making the use of personal protective equipment a standard in efforts to stop the spread of disease." The piece connects that historical lesson to the present, noting that new, more contagious coronavirus strains "only further underlines the need for masks and other personal protective equipment," implying pandemics prompt both innovation and adoption of measures that aid recovery and future prevention.
```

**Tokens:** {'completion_tokens': 1284, 'prompt_tokens': 2241, 'total_tokens': 3525, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 1152, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 2176}, 'latency_checkpoint': {'engine_tbt_ms': 11, 'engine_ttft_ms': 41, 'engine_ttlt_ms': 13656, 'pre_inference_ms': 153, 'service_tbt_ms': 11, 'service_ttft_ms': 581, 'service_ttlt_ms': 14165, 'total_duration_ms': 14021, 'user_visible_ttft_ms': 428}}

## Config C - C (chunk=256, overlap=0.10)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.4621 | 120 | The Manchurian Plague |
| 2 | 0.4474 | 29 | How to Be Productive and Creative in Times of Panic |
| 3 | 0.4457 | 11 | Facing Three Fundamental Coronavirus Fears |
| 4 | 0.4394 | 142 | Subject, Consumer, or Citizen: Three Post-Covid Futures |
| 5 | 0.4332 | 108 | Being Well Pub Launches Medika to Expand Our Writers’ Reach |

### gpt-5-mini response

```
I don't know based on the provided Medium articles data.
```

**Tokens:** {'completion_tokens': 405, 'prompt_tokens': 2178, 'total_tokens': 2583, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 384, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 11, 'engine_ttft_ms': 77, 'engine_ttlt_ms': 4819, 'pre_inference_ms': 167, 'service_tbt_ms': 11, 'service_ttft_ms': 620, 'service_ttlt_ms': 5448, 'total_duration_ms': 5287, 'user_visible_ttft_ms': 454}}

## Config D - D (chunk=1024, overlap=0.30)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.4663 | 120 | The Manchurian Plague |
| 2 | 0.4398 | 29 | How to Be Productive and Creative in Times of Panic |
| 3 | 0.4250 | 11 | Facing Three Fundamental Coronavirus Fears |
| 4 | 0.4150 | 142 | Subject, Consumer, or Citizen: Three Post-Covid Futures |
| 5 | 0.3913 | 70 | Only 49% of Americans Plan to Get Vaccinated Against COVID-19. Yes, You Should Be That Shocked |

### gpt-5-mini response

```
The Manchurian Plague (Ben Kageyama) argues that past pandemics drive practical innovations and public-health changes that aid recovery. The article says the 1910 Manchurian Plague “was an event widely credited for making the use of personal protective equipment a standard in efforts to stop the spread of disease,” using that historical example to show how outbreaks prompt lasting change. Kageyama links this lesson to the present, noting a new, more contagious coronavirus strain and saying that history “only further underlines the need for masks and other personal protective equipment.”
```

**Tokens:** {'completion_tokens': 1024, 'prompt_tokens': 2222, 'total_tokens': 3246, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 896, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 12, 'engine_ttft_ms': 71, 'engine_ttlt_ms': 12207, 'pre_inference_ms': 539, 'service_tbt_ms': 11, 'service_ttft_ms': 1643, 'service_ttlt_ms': 13671, 'total_duration_ms': 13137, 'user_visible_ttft_ms': 1103}}
