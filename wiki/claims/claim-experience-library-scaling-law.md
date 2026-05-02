---
title: "LLM-agent performance follows a scaling law in experience-library size"
slug: claim-experience-library-scaling-law
status: weakly_supported
confidence: 0.55
tags:
  - self-evolving-agents
  - llm-agents
  - scaling-laws
  - continual-learning
domain: "NLP"
source_papers:
  - flex-continuous-agent-evolution-forward-learning
evidence:
  - source: flex-continuous-agent-evolution-forward-learning
    type: supports
    strength: moderate
    detail: "On GSM8k (5 epochs), train accuracy rises 81.2% to 94.2% as library grows 1,001 to 1,904 entries with a power-law fit; test accuracy rises 81.3% to 83.3% with reduced variance; library growth itself is logistic-like (rapid then selective)."
conditions: "Frozen capable base LLM; well-curated experience updater; benchmark-specific library schema (hierarchical for AIME25/USPTO50k, flat for GSM8k/ProteinGym)."
date_proposed: 2026-05-02
date_updated: 2026-05-02
---

## Statement

There exists a predictable scaling relationship between the size of an LLM agent's experience library and its downstream task performance: as the library grows under a forward-learning update rule, training accuracy follows a power law, generalization improves with reduced variance, and the library's own growth follows a logistic-like saturation curve.

## Evidence summary

The supporting evidence comes from a single paper (FLEX), GSM8k only, across 5 epochs. Three regimes are reported:

- training accuracy vs. library size — power-law fit, 81.2% to 94.2% as library grows 1,001 to 1,904;
- test accuracy vs. library size — monotone improvement 81.3% to 83.3% (above 80.8% baseline) with shrinking variance;
- library size vs. epoch — rapid growth early (+576 epoch 1 to 2) then selective refinement (+64 epoch 4 to 5), suggesting a logistic-like saturation.

This is consistent with the hypothesis but rests on one base model on one benchmark; statistical significance and confidence intervals are not reported.

## Conditions and scope

- Holds when the base LLM is sufficiently capable to use distilled experiences (FLEX's information-theoretic derivation assumes $\pi(\cdot \mid X, \varepsilon) \approx p^*(\cdot \mid X, \varepsilon)$).
- Holds when the updater agent is well-calibrated and prevents redundant accumulation.
- Library schema (hierarchical / flat / dual-zone) is hand-chosen per benchmark; the scaling regime under arbitrary schema is unknown.
- Reported only for $\mathcal{E}$ in the 1k-2k range; behavior at much larger library sizes (1e5+) is untested.

## Counter-evidence

None directly. Indirectly: prior memory-based agents (Memento, ReasoningBank) have shown diminishing-returns plateaus from raw-trajectory accumulation, suggesting that the FLEX scaling law may depend critically on the *distillation* step, not on raw memory growth.

## Linked ideas

(none yet)

## Open questions

- Does the law hold across different base-LLM scales (1B vs. 70B vs. closed-frontier)?
- Are the exponents domain-invariant or task-dependent?
- At what library size does generalization saturate or degrade due to retrieval noise?
- How does the law interact with multi-source library mixing?
