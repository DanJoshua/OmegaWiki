---
title: "Suggestibility Metric"
aliases:
  - suggestibility
  - model suggestibility
  - LLM suggestibility
tags:
  - agent-memory
  - in-context-learning
  - agent-adaptation
  - model-behavior
maturity: emerging
key_papers:
  - learning-supervision-semantic-episodic-memory-reflective
first_introduced: "Hassell et al. (2025)"
date_updated: 2026-05-07
related_concepts:
  - test-time-learning
  - self-evolving-memory
---

## Definition

**Suggestibility** is a model-level metric that quantifies how receptive a language model is to external reasoning provided in its context window. A model with high suggestibility updates its behavior substantially when critique-encoded guidance is present; a model with low suggestibility largely ignores contextual feedback and defaults to its parametric priors regardless of quality.

Formally, suggestibility is measured as the fraction of cases where a model follows the reasoning direction encoded in a retrieved memory entry (e.g., a critique asserting the correct answer and explanation) over the fraction of cases where it would have reached the same conclusion anyway. High suggestibility is a necessary condition for memory-augmented adaptation to yield accuracy gains.

## Intuition

Not all models benefit equally from in-context memory. Scale alone does not determine suggestibility: a large model that has strong parametric priors may be less willing to follow external critique than a smaller model with weaker priors. Suggestibility separates the question "is the model capable?" from the question "can external signals steer the model?". It explains why some models gain 20+pp from critique-grounded memory while others gain near zero.

## Variants

- **Attribution-conditioned suggestibility**: the same model shows higher suggestibility when critiques are attributed to a user than when attributed to itself or another model — suggesting the perceived source of feedback affects internalization.
- **Domain-specific suggestibility**: fact-heavy domains (PubMed) suppress suggestibility even in otherwise high-suggestibility models, because the model's parametric confidence resists override.

## Known limitations

- Suggestibility is measured post-hoc from experimental outcomes, not predicted from model weights or architecture.
- High suggestibility can be a liability: a highly suggestible model is also more vulnerable to adversarial or low-quality memory entries.
- The metric as defined requires labeled test data to compute; not applicable in unsupervised or streaming settings without modification.

## Open problems

- Can suggestibility be predicted from pretraining data or RLHF alignment procedure without running experiments?
- What is the causal mechanism? (Attention head specialization? RLHF-induced deference to human-attributed signals?)
- Is there an optimal suggestibility level that balances adaptability and robustness to noise?

## Key papers

- [[learning-supervision-semantic-episodic-memory-reflective]] — introduces the metric and uses it to explain variance in memory-augmented adaptation gains.

## My understanding

Suggestibility is an underappreciated axis in the in-context learning literature. Most benchmark papers report aggregate gains across models without asking why some models respond and others do not. This metric gives a handle on that variance. The finding that attribution (user vs. self vs. other model) affects suggestibility is especially interesting — it implies alignment training shapes not just content but the model's epistemic deference to different signal sources.
