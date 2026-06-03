# Q3 key idea summary

**Question:** Find an article that argues past pandemics (such as the bubonic plague) can spur innovation and recovery, and summarise its central argument.

**top_k:** 8  |  **embedding:** `4UHRUIN-text-embedding-3-small`  |  **chat:** `4UHRUIN-gpt-5-mini`

## Config A - A (chunk=512, overlap=0.15)

### Retrieved articles (deduped on article_id, top 5)

| rank | score | article_id | title |
|---|---|---|---|
| 1 | 0.4619 | 120 | The Manchurian Plague |
| 2 | 0.4507 | 11 | Facing Three Fundamental Coronavirus Fears |
| 3 | 0.4480 | 142 | Subject, Consumer, or Citizen: Three Post-Covid Futures |
| 4 | 0.4311 | 173 | I Hope This Pandemic Has Taught Us That Products Can’t Replace People |
| 5 | 0.4253 | 29 | How to Be Productive and Creative in Times of Panic |

### gpt-5-mini response

```
Article: "The Manchurian Plague" by Ben Kageyama.

Summary: The article argues that the 1910 Manchurian plague spurred lasting public‑health innovation, noting it "was an event widely credited for making the use of personal protective equipment a standard in efforts to stop the spread of disease." It describes Dr. Wu Lien‑teh’s "main approach" — "an emphasis on the wearing of cloth face masks and other personal protective equipment" — plus harsh quarantines and travel restrictions. The piece concludes that these measures "contained" the outbreak to Manchuria rather than letting it become nationwide, showing how a pandemic can drive practical innovations and recovery in public health.
```

**Tokens:** {'completion_tokens': 1179, 'prompt_tokens': 2175, 'total_tokens': 3354, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 1024, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 10, 'engine_ttft_ms': 63, 'engine_ttlt_ms': 12125, 'pre_inference_ms': 136, 'service_tbt_ms': 10, 'service_ttft_ms': 582, 'service_ttlt_ms': 12639, 'total_duration_ms': 12513, 'user_visible_ttft_ms': 446}}

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
Article: "The Manchurian Plague" by Ben Kageyama.

Summary: The piece argues that past pandemics can drive lasting public‑health innovations: it cites the 1910 Manchurian Plague as “an event widely credited for making the use of personal protective equipment a standard in efforts to stop the spread of disease.” The author uses that historical example to underline current lessons for COVID‑19 — “only further underlines the need for masks and other personal protective equipment” — showing how outbreaks can change practice and spur protective measures.
```

**Tokens:** {'completion_tokens': 764, 'prompt_tokens': 2241, 'total_tokens': 3005, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 640, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'latency_checkpoint': {'engine_tbt_ms': 10, 'engine_ttft_ms': 83, 'engine_ttlt_ms': 7712, 'pre_inference_ms': 147, 'service_tbt_ms': 10, 'service_ttft_ms': 601, 'service_ttlt_ms': 8226, 'total_duration_ms': 8091, 'user_visible_ttft_ms': 454}}
