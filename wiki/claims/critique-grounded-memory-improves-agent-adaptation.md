---
title: "Critique-grounded episodic+semantic memory improves agent task accuracy without parameter updates"
slug: "critique-grounded-memory-improves-agent-adaptation"
status: weakly_supported
confidence: 0.65
tags:
  - agent-memory
  - episodic-memory
  - semantic-memory
  - test-time-learning
  - parameter-free-adaptation
domain: NLP
source_papers:
  - learning-supervision-semantic-episodic-memory-reflective
evidence:
  - source: learning-supervision-semantic-episodic-memory-reflective
    type: supports
    strength: moderate
    detail: "EP+SEM_CRIT yields average +8.1pp over zero-shot and +4.6pp over RAG-style baseline across 6 datasets and 7 models; peak gain +24.8pp on PubMed. Gains vary substantially by model suggestibility and domain structure."
conditions: "Holds when (1) model suggestibility is sufficiently high, (2) supervision provides labeled examples from which critique rationales generalize across test examples, (3) task domain has sufficient within-cluster similarity for episodic retrieval. Does not hold for low-suggestibility models, domains with low cross-instance critique transfer, or reasoning models that already perform critique-like reasoning internally."
date_proposed: 2026-05-07
date_updated: 2026-05-07
---

## Statement

LLM agents can achieve meaningful accuracy improvements on classification tasks by storing label-grounded critiques (structured as assertion + rationale + reflection) in episodic and semantic memory, and retrieving them at test time — without any parameter updates. The combined episodic+semantic strategy outperforms both zero-shot baselines and RAG-style few-shot baselines that rely only on raw labels.

## Evidence summary

Single paper with controlled ablations across 6 datasets and 7 models. The +8.1pp improvement over zero-shot and +4.6pp over EP_LABEL (RAG with labels only) demonstrates that the critique structure adds meaningful signal beyond label examples alone. The finding is moderated by model suggestibility — without sufficient receptivity to contextual reasoning, gains collapse to near zero (Llama 4 Scout). Status is weakly_supported pending replication by independent groups.

## Conditions and scope

- Supervised classification with access to a labeled training set for offline critique generation.
- Memory benefit scales with model suggestibility; requires measuring or estimating suggestibility before deployment.
- Episodic memory dominates semantic memory when training data is abundant; semantic memory preferred under sparse supervision with frequent inference.
- Efficiency corollary: critique-loaded memory reduces thinking tokens for reasoning models by ~32%, suggesting an orthogonal benefit even where accuracy gains are modest.

## Counter-evidence

- Gains disappear for low-suggestibility models (Llama 4 Scout, 56.2% suggestibility).
- Reasoning models on preference datasets already perform internal critique-like reasoning over retrieved examples; explicit critique storage adds near-zero accuracy for them (though token efficiency benefits persist).
- Fact-intensive domains with low cross-instance transfer (PubMed under Qwen3) show limited gains.

## Linked ideas

## Open questions

- Does this generalize to open-ended generation or multi-turn dialogue beyond classification?
- What happens when the labeled supervision itself contains errors? Is the critique generation robust to noisy labels?
- Can the efficiency benefit (token reduction) be achieved without the accuracy overhead of critique pre-computation?
